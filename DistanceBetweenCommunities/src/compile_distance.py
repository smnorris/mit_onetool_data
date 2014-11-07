"""
directions.py

Given a list of places, query the google directions api for driving time and
distance between all combinations of places - generate an origin-distance table

Script handles input csv file as obtained from GeoBC, can be tweaked for a more
general input file.

Writes to output csv:
- origin id
- origin name
- destination id
- destination name
- route summary
- driving distance (to the nearest km)
- driving duration (rounded to 10min)
"""

import urllib
import urllib2
import json
import os
import csv
from collections import OrderedDict
import time


_GOOGLE_DIRECTIONS_QUERY_URL = 'http://maps.googleapis.com/maps/api/directions/json?'
MAPQUEST_URL = r'http://open.mapquestapi.com/directions/v2/route?'
MAPQUEST_KEY = 'Fmjtd%7Cluur2l08l9%2C2w%3Do5-9a7au0'
_MAPQUEST_ROUTE_SERVICE_URL = MAPQUEST_URL

INTERVALS = OrderedDict([("Y", 365*86400),  # 1 year
                         ("M", 30*86400),   # 1 month
                         ("W", 7*86400),    # 1 week
                         ("D", 86400),      # 1 day
                         ("h", 3600),       # 1 hour
                         ("m", 60),         # 1 minute
                         ("s", 1)])         # 1 second


def seconds_to_human(seconds):
    """Convert seconds to human readable format,
       rounding to nearest 10min

    :param seconds: Seconds to convert
    :type seconds: int

    :rtype: int
    :return: Human readable string
    """
    # round to nearest 10min
    seconds = int((seconds + 300) // 600 * 600)
    string = ""
    for unit, value in INTERVALS.items():
        subres = seconds / value
        if subres:
            seconds -= value * subres
            string += str(subres) + unit
    return string


def fetch_json(query_url, params={}, key=None):
    encoded_params = urllib.urlencode(params)
    url = query_url + encoded_params
    if key:
        url = url+"&key="+key
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return (url, json.load(response))


def google_directions_query(origin, destination):
    params = {'origin':  origin,
              'destination': destination,
              'sensor': 'false'}
    url, response = fetch_json(_GOOGLE_DIRECTIONS_QUERY_URL, params=params)
    status = response['status']
    if status == 'OK':
        # let's presume all routes have just one leg
        # fort nelson to victoria is one leg, as is masset to fernie
        summary = response['routes'][0]['summary']
        route = response['routes'][0]['legs'][0]
        durationSeconds = route['duration']['value']
        durationMin = durationSeconds / 60
        durationTxt = seconds_to_human(route['duration']['value'])
        distKm = int(round(route['distance']['value'] / 1000))
        return (status,
                origin, destination, summary, distKm, durationTxt, durationMin)
    else:
        return (status, origin, destination, None, None, None, None)


def mapquest_directions_query(origin, destination):
    """
    Try querying the mapquest open directions service

    Note that mapquest doesn't offer a small summary of the route
    (however, there are LOTS of other options... see
     http://open.mapquestapi.com/directions)
    There is even an option to return a 'route matrix', but lets not bother
    with that, we already have this code for deriving that.
    """
    params = {'from': origin,
              'to': destination,
              'unit': 'k'}
    url, response = fetch_json(_MAPQUEST_ROUTE_SERVICE_URL,
                               params=params,
                               key=MAPQUEST_KEY)
    status = response['info']['statuscode']
    if status == 0:
        durationSeconds = response['route']['time']
        durationMin = durationSeconds / 60
        durationTxt = seconds_to_human(durationSeconds)
        distance = int(round(response['route']['distance']))
        ferry = response['route']['hasFerry']
        return (status,
                origin,
                destination, None, distance, durationTxt, durationMin, ferry)
    else:
        return (status,
                origin,
                destination,
                response['info']['messages'], None, None, None, None)


def test():
    # test coordinates as input (taken from internet)
    victoria = "48.428613,-123.364912"
    vancouver = "49.283241,-123.119303"

    print mapquest_directions_query(victoria, vancouver)
    print google_directions_query(victoria, vancouver)

    # test text as input
    #print google_directions_query("Duncan BC", "Victoria BC")
    #print google_directions_query("Langford BC", "Vancouver BC")
    #print google_directions_query("Williams Lake BC", "Prince George BC")
    #print google_directions_query("Fort Nelson BC", "Victoria BC")
    #print google_directions_query("Masset BC", "Fernie BC")


def parse_csv_rec(rec):
    origID = rec["CSD_UID"]
    origName = rec['OFFNAME']
    lon = rec['REPPOINT_LONGITUDE']
    lat = rec['REPPOINT_LATITUDE']
    origCoord = lat+","+lon
    return (origID, origName, origCoord)


def process_list():
    # define path to project
    project = os.path.join(os.environ['PROJECTS'], r"mit/OneToolDataPrep")
    path = os.path.join(project, "deliverable/scripts/MapQuest_Google")

    # open a list of all communities (list is from geobc)
    # Test with incorporated areas:
    # towns, district municipalities, villages, cities, island municipality, nisgaa land, regional municipality,
    incorporatedAreas = {'CY': 'City',
                         'DM': 'District Municipality',
                         'IM': 'Island Municipality',
                         'NL': "Nisga'a Land",
                         'RGM': 'Regional Municipality',
                         'T': 'Town',
                         'VL': 'Village',
                         'T': 'Town'}
    placesCSV = os.path.join(path, "csd_locations.csv")
    places = [row for row in csv.DictReader(open(placesCSV, 'rb')) if row["OFF_CSDTYPE"] in incorporatedAreas.keys()]
    places = sorted(places, key=lambda places: places["OFFNAME"])
    # for testing, use just the first several places in the list
    places = places[:10]

    # define output file
    outFile = os.path.join(path, "testOutput.csv")

    with open(outFile, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        # write header
        writer.writerow(("ORIGIN_ID", "ORIGIN_NAME",
                         "DESTINATION_ID", "DESTINATION_NAME",
                         "MAPQUEST_KM", "MAPQUEST_TIME", "MAPQUEST_MIN",
                         "MAPQUEST_FERRY", "MAPQUEST_ERROR", "GOOGLE_ROUTE",
                         "GOOGLE_KM", "GOOGLE_TIME", "GOOGLE_MIN"))
        for i, originRec in enumerate(places):
            origId, origName, origCoord = parse_csv_rec(originRec)
            for destRec in places[i + 1:]:
                destId, destName, destCoord = parse_csv_rec(destRec)
                gStatus, o, d, gRoute, gKm, gTimeTxt, gTimeMin = google_directions_query(origCoord, destCoord)
                mqStatus, o, d, mqMessage, mqKm, mqTimeTxt, mqTimeMin, mqFerry = mapquest_directions_query(origCoord, destCoord)
                writer.writerow((origId, origName, destId, destName, mqKm,
                                 mqTimeTxt, mqTimeMin, mqFerry, mqMessage, gRoute, gKm, gTimeTxt, gTimeMin))
                print (mqStatus, gStatus, origName, destName)
                time.sleep(.25)

#test()
process_list()

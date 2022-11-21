# from amadeus import Client, ResponseError, Location
#
# amadeus = Client(
#     client_id='GoJxdZIivaehEX52UiZVUlGS7Ob0sm6H',
#     client_secret='tFOeUaHd2sKASvqd'
# )
#
# def get_city_airport_list(data):
#     result = []
#     for i, val in enumerate(data):
#         result.append(data[i]['iataCode']+', '+data[i]['name'])
#     result = list(dict.fromkeys(result))
#     return result
#
#
# try:
#     # response = amadeus.reference_data.locations.get(keyword="GDL", subType=Location.ANY)
#     response = amadeus.shopping.flight_offers_search.get(
#         originLocationCode='GDL',
#         destinationLocationCode='SEA',
#         departureDate='2022-11-20',
#         adults=1)
#
#     print(response.data[0])
# except ResponseError as error:
#     print(error)


# Python program to read
# json file


import json
f = open('testdata.json')
data = json.load(f)
for i,x in data.items():
    print(i,x)
f.close()
print()
print({
    'salida':data['itineraries'][0]['segments'][0]['departure']['iataCode'],
    'llegada':data['itineraries'][0]['segments'][0]['arrival']['iataCode'],
    'tsalida':data['itineraries'][0]['segments'][0]['departure']['at'].partition('T')[2][:-3:],
    'tllegada':data['itineraries'][0]['segments'][0]['arrival']['at'].partition('T')[2][:-3:],
    'precio': data['price']['grandTotal'] + ' ' + data['price']['currency']
})
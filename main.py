from amadeus import Client, ResponseError, Location

amadeus = Client(
    client_id='FaziC540ZOEICHriFUkwxAagokRDlCkA',
    client_secret='c1JehzWtYBbA0eUQ',
    # log_level='debug'
)
#
def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode']+', '+data[i]['name'])
    result = list(dict.fromkeys(result))
    return result


# try:
#     # response = amadeus.reference_data.locations.get(keyword="GDL", subType=Location.ANY)
#     # response = amadeus.shopping.flight_offers_search.get(
#     #     originLocationCode='GDL',
#     #     destinationLocationCode='SEA',
#     #     departureDate='2022-11-20',
#     #     adults=1)
#     response = amadeus.reference_data.locations.hotels.by_city.get(cityCode='GDL', radius=100)
#
#     print(response.data)
# except ResponseError as error:
#     print(error.description())


try:
    # response = amadeus.reference_data.locations.get(keyword="GDL", subType=Location.ANY)
    # response = amadeus.shopping.flight_offers_search.get(
    #     originLocationCode='GDL',
    #     destinationLocationCode='SEA',
    #     departureDate='2022-11-20',
    #     adults=1)
    # response = amadeus.shopping.hotel_offers.get(hotelIds=list('HIGDL03B'), adults=1)
    # response = amadeus.shopping.hotel_offers_by_hotel.get(hotelId='BGLONBGB')

    response = amadeus.shopping.hotel_offers_search.get(hotelIds='FHGDLCC1', checkInDate='2022-12-01', checkOutDate='2022-12-15', adults='2')

    print(response.data[0]['offers'])
except ResponseError as error:
    print(error)


# Python program to read
# json file


# import json
# f = open('testdata.json')
# data = json.load(f)
# for i,x in data.items():
#     print(i,x)
# f.close()
# print()
# print({
#     'salida':data['itineraries'][0]['segments'][0]['departure']['iataCode'],
#     'llegada':data['itineraries'][0]['segments'][0]['arrival']['iataCode'],
#     'tsalida':data['itineraries'][0]['segments'][0]['departure']['at'].partition('T')[2][:-3:],
#     'tllegada':data['itineraries'][0]['segments'][0]['arrival']['at'].partition('T')[2][:-3:],
#     'precio': data['price']['grandTotal'] + ' ' + data['price']['currency']
# })
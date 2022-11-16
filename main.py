from amadeus import Client, ResponseError, Location

amadeus = Client(
    client_id='GoJxdZIivaehEX52UiZVUlGS7Ob0sm6H',
    client_secret='tFOeUaHd2sKASvqd'
)

def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode']+', '+data[i]['name'])
    result = list(dict.fromkeys(result))
    return result


try:
    response = amadeus.reference_data.locations.get(keyword="GDL", subType=Location.ANY)
    print(response.data)
    print(get_city_airport_list(response.data))
except ResponseError as error:
    print(error)
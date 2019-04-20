import pandas as pd

def data():
    raw_data = pd.read_csv('raw-flight-segment-data.csv')

    # filter only passenger flights
    raw_data = raw_data[raw_data['PASSENGERS'] > 0]

    # filter only segments with at least a daily flight
    # the dataset contain one month of data, so that translate to at least 30 flights performed
    raw_data = raw_data[raw_data['DEPARTURES_PERFORMED'] > 30]
    # calculate the pre flight air time
    raw_data['AIR_TIME'] = raw_data['AIR_TIME'] / raw_data['DEPARTURES_PERFORMED']

    # filter only major airports
    # an airport code that contains number is usually assigned to minor airport with limited commercial service
    raw_data = raw_data[~raw_data['ORIGIN'].str.contains('.*[0-9].*')]
    raw_data = raw_data[~raw_data['DEST'].str.contains('.*[0-9].*')]

    # select the relevant columns
    raw_data = raw_data[['DISTANCE', 'AIR_TIME', 'ORIGIN', 'ORIGIN_CITY_NAME', 'DEST','DEST_CITY_NAME']]

    # drop NaN values
    raw_data = raw_data.dropna()


    # group by origin and destination with give us the flight segments
    # there might be multiple airlines running the same segment
    # in such case we will simply go with the first airline
    data = raw_data.groupby(['ORIGIN', 'DEST']).first()
    print ("Total segments: {:d}".format(data.shape[0]))


if __name__ == "__main__":
    data()

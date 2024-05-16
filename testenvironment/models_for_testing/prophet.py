import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from prophet import Prophet

from all_models_for_testing.general_ml_model import GeneralModel

'''
https://facebook.github.io/prophet/docs/quick_start.html
'''
class ProphetModel(GeneralModel):


    def run(self):

        # Convert numpy array to DataFrame
        transposed_data = self.data.T
        m = [i for i in range(len(self.data[0]))]

        test = [m] + self.data.tolist()

        test = np.array(test)

        df = pd.DataFrame(test.T, columns=['ds', 'y', 'humidity', 'wind_speed', "meanpressure"])
        start_date = '1970-01-01'
        df['ds'] = pd.date_range(start=start_date, periods=len(df), freq='D')
        # Visualize the data
        plt.plot(df['ds'], df['y'])
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title('Time Series trend')
        plt.show()

        # Create a Prophet object and fit it to the data
        model = Prophet()
        model.fit(df)

        # Create a future dataframe
        future = model.make_future_dataframe(periods=365)

        # Make predictions for the future dates
        forecast = model.predict(future)

        print(forecast)

        # Visualize the predictions
        plt.plot(forecast['yhat_lower'])
        plt.plot(forecast['yhat'])
        plt.plot(forecast['yhat_upper'])
        plt.plot(forecast['trend'])
        plt.plot(self.data[0])

        forecast.plot()
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title('Forecast for the Next Year')
        plt.show()

        # Using additional regressors
        future_data = df[df.ds > '1970-11-01']
        train_data = df[df.ds <= '1970-11-01']

        m = Prophet()
        m.add_regressor('humidity')
        m.add_regressor('wind_speed')
        m.add_regressor('meanpressure')
        m.fit(train_data)

        # Make predictions for the future dates with additional regressors
        forecast_regressors = m.predict(future_data)
        print(forecast_regressors[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

        print("______________________")
        print(forecast_regressors["yhat"])
        # Visualize the predictions with additional regressors
        plt.plot(forecast_regressors['yhat'])
        plt.plot(forecast_regressors['yhat_lower'])
        plt.plot(forecast_regressors['yhat_upper'])
        #plt.plot(self.data[0])
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title('Forecast using Multiple Regressors')
        plt.show()

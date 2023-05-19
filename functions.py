from utils.libraries import *
import math

def open_file(PATH):
    try:
        data = pd.read_csv(PATH)
    except:
        print("Couldn't Open CSV File. Trying for EXCEL.")
        try:
            data = pd.read_excel(PATH)
        except:
            print("Couldn't Open EXCEL File")
        else:
            return data
    else:
        return data

def plot_data(data, original_columns):
    # Showing Data
    plt.figure(figsize=(15, 3))
    plt.title(original_columns[0] + " Vs" + original_columns[1], fontsize=20, fontweight="bold")
    plt.plot(data['ds'], data['y'])
    plt.xticks(rotation=30, ha='right')
    plt.xlabel(original_columns[0])
    plt.ylabel(original_columns[1])
    st.pyplot(plt)

def plot_components(data):
    model = st.selectbox("***Type of seasonal component***",
                        ["additive", "multiplicative"])
    period = st.slider("**Period of the series**", 1, math.floor(data.shape[0]/2), math.floor(data.shape[0]/2))
    data.set_index('ds', inplace=True)
    result = seasonal_decompose(data['y'], period=period, model=model)
    plt.figure(figsize=(15, 3))
    plt.title("Trend", fontsize=20, fontweight="bold")
    result.trend.plot()
    plt.title("Trend", fontsize=20, fontweight="bold")
    result.trend.plot()
    plt.show()
    st.pyplot(plt)
    st.markdown("***Trend***: Describes whether the time series is decreasing, constant, or increasing over time.")
    plt.figure(figsize=(15, 3))
    plt.title("Seasonality", fontsize=20, fontweight="bold")
    result.seasonal.plot()
    plt.show()
    st.pyplot(plt)
    st.markdown("***Seasonality***: Describes the periodic signal in your time series.")
    plt.figure(figsize=(15, 3))
    plt.title("Noise", fontsize=20, fontweight="bold")
    result.resid.plot()
    plt.show()
    st.pyplot(plt)
    st.markdown("***Noise***: Describes what remains behind the separation of seasonality and trend from the time series. In other words, it's the variability in the data that cannot be explained by the model.")

def evaluation(y, yhat):
    dict_ = {
        "Mean Absolute Error": [mean_absolute_error(y, yhat)],
        "Mean Absolute Percentage Error": [mean_absolute_percentage_error(y, yhat)],
        "Mean Square Error": [mean_squared_error(y, yhat)],
        "Root Mean Square Error": [math.sqrt(mean_squared_error(y, yhat))]
    }
    metrics = pd.DataFrame(dict_)
    metrics.index = ["Values"]
    return metrics

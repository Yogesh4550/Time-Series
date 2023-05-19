from utils.libraries import *
from utils.functions import *

def future(data):
    st.markdown("""### Let's Forecast""")
    file_name = st.text_input("**Enter File Name**")
    days = st.slider ("**How many Days?**", 1, 365, 30)
    tell = st.button("Tell me the Future")
    
    if tell:
        with open('./saved_model/prophet_model.json', 'r') as fin:
            model = model_from_json(fin.read()) # Load model
        
        with open('./saved_model/model_config.pkl', 'rb') as file:
            config = pickle.load(file)
        
        YES_CAP = config["YES_CAP"]
        MAX = config["MAX"]
        MIN = config["MIN"]
        
        future = model.make_future_dataframe(periods=days, include_history=False)
        
        if YES_CAP:
            future['cap'] = MAX
            future['floor'] = MIN
        
        forecast = model.predict(future)
        
        fig = model.plot(forecast)
        a = add_changepoints_to_plot(fig.gca(), model, forecast)
        
        st.pyplot(fig)
        
        forecast[['ds', 'yhat']].to_csv("./forecast/" + file_name + ".csv", index=False)
        st.success("Your Forecast is Saved Successfully...")

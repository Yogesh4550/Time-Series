from utils.libraries import *
from utils.functions import *
from utils.train import train_model
from utils.predict import future


def main(PATH):
    data = open_file(PATH)
    original_columns = data.columns.tolist()

    # Data Cleaning and Formatting 
    data.columns = ['ds', 'y']
    data['ds'] = pd.to_datetime(data['ds'])
    data.dropna(inplace=True)

    tabl, tab2, tab3, tab4, tab5 = st.tabs(["Data", "Train Model", "Model Evaluation", "Model Components", "Forecast"])

    with tabl:
        st.markdown("""### Your Data """)
        plot_data(data, original_columns)
        st.markdown("""### Components""")
        comp_data = data.copy()
        plot_components(comp_data)
        
        SET_NONE_DATA = st.checkbox("**Do you want to Remove Unusual Event from Data?**")
        backup_data = data.copy()
        if SET_NONE_DATA:
            start_date = st.date_input("Enter Start Date")
            end_date = st.date_input("Enter End Date")
            data.loc[(data['ds'] > start_date.strftime("%Y-%m-%d")) & (data['ds'] < end_date.strftime("%Y-%m-%d")), 'y'] = None
            plot_data(data, original_columns)
        
        REMOVE_OUTLIERS = st.checkbox ("**Do you want to remove Outliers?**")
        if REMOVE_OUTLIERS:
            # Outlier Imputation with rolling median 
            window_size = st.slider("**Window Size**", 1, 100, 5)
            threshold = st.slider("**Threshold**", 1, 100, 3)
            data['y'] = hampel(data['y'], window_size=window_size, n=threshold, imputation=True)
            st.markdown(""" ### Your data after removing outliers""")
            plot_data(data, original_columns)

    with tab2: 
        st.markdown("""## Choose your model Configuration""")
        model, forecast, step1 = train_model(data)
        
    with tab3:
        if step1:
            st.markdown("""### Model Plot""")      
            fig = model.plot(forecast)
            add_changepoints_to_plot(fig.gca(), model, forecast)
            st.pyplot(fig)
            st.markdown("### Scores") 
            st.dataframe(evaluation(backup_data[['y']], forecast[['yhat']]).T)
        else:
            st.write("Please Train the Model.")
    
    with tab4:
        if step1: 
            st.markdown("""### Model Components""")
            fig2 = model.plot_components(forecast)
            st.pyplot(fig2)
        else:
            st.write("Please Train the Model.")
    
    with tab5: 
        future(data)
        

if __name__ == '__main__':
    st.title("Forecasting with Facebook's Prophet")
    st.sidebar.markdown("""## Upload Data""")
    PATH = st.sidebar.file_uploader('')

    if PATH is None:
        st.write("Please Select Data from Sidebar:")
    else:
        main(PATH)

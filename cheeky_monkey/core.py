# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = []

# Cell
import pandas as pd

# Internal Cell


def from_dob_to_age(row, born_fld, as_of_date_fld):
    born = row[born_fld]
    as_of_date = row[as_of_date_fld]
    years = as_of_date.year - born.year - ((as_of_date.month, as_of_date.day) < (born.month, born.day))


    if (as_of_date.day == born.day):
        if as_of_date.month - born.month -1 < 0:
            months = 12 + (as_of_date.month - born.month  )
        else:
            months = as_of_date.month - born.month

    elif (as_of_date.day <  born.day):
        if as_of_date.month - born.month -1 < 0:
            months = 12 + (as_of_date.month - born.month -1 )
        else:
            months = as_of_date.month - born.month
    else:
        if as_of_date.month - born.month < 0:
            months = 12 + (as_of_date.month - born.month -1 )
        else:
            months = as_of_date.month - born.month

    if months >= 10.0:
        reporting_age = years + 1
    else:
        reporting_age = years

    if (reporting_age % 2) == 1:
        age_bucket = int(reporting_age) -1
    else:
        age_bucket = int(reporting_age)

    adjustedbirthdate = born + pd.offsets.DateOffset(years=years)

    bd_period = pd.Period(adjustedbirthdate, freq='D')
    as_of_date_period=  pd.Period(as_of_date, freq='D')

    days_to_birthdate = bd_period.day_of_year - as_of_date_period.day_of_year
    if days_to_birthdate < 0.0:
        days_to_birthdate = days_to_birthdate + 365
    return years, months, reporting_age, age_bucket, days_to_birthdate

# Internal Cell
def derive_statuscount_percase(df_in, ftedays_df):
    "do some calculations"
    FTE_DAYS_YEAR = ftedays_df['FTE (Days)'].sum()
    print('FTE_DAYS_YEAR', FTE_DAYS_YEAR)
    aggregation = {
        'Case Count': ('STATUS_COUNT','size'),
        'Total Status Change Count': ('STATUS_COUNT','sum')
    }

    # df = df_in.groupby(['ORIGIN_DSC']) \
    # .agg(** aggregation).reset_index()

    # aggregation = {
    #     'Case Count': ('DRIVERS_LICENSE_NO','size'),
    #     'Status Count': ('STATUS_COUNT','sum'),
    #     }

    df = df_in.groupby([pd.Grouper(freq='M', key='CASE_OPENED_DT') ,
                                pd.Grouper(key='ORIGIN_DSC'),
                                ]).agg(** aggregation)

    df = pd.DataFrame(df).reset_index()

    df['Opened Month'] = df.apply(lambda x: x['CASE_OPENED_DT'].strftime('%b') + '-' + x['CASE_OPENED_DT'].strftime('%Y'), axis=1)

    #case_summary_data['Total Cases in Group'] = case_summary_data.groupby(['Origin Report'])['Cases'].transform(lambda x: sum(x) )
    df['Total Cases In Month'] = df.groupby(['CASE_OPENED_DT'])['Case Count'].transform( lambda x: sum(x))
    df['Total Status Changes In Month'] = df.groupby(['CASE_OPENED_DT'])['Total Status Change Count'].transform( lambda x: sum(x))
    df['Monthly Status Changes/Case'] = df.apply(lambda x: x['Total Status Changes In Month']/x['Total Cases In Month']  , axis=1)


    df['Group Status Changes/Case'] = df.apply(lambda x: x['Total Status Change Count']/x['Case Count']  , axis=1)
    #Month-Year	FTE (Days)
    df = pd.merge(df, ftedays_df, how='left',  left_on='Opened Month', right_on='Month')
    #df = df[df['Is Adjudicated'] == 'Adjudicated']
    print('df shape ', df.shape)
    case_count = df['Case Count'].sum()
    status_change_count = df['Total Status Change Count'].sum()

    df['Group Case Count/FTE'] = df.apply(lambda x: x['Case Count']/x['FTE (Days)']  , axis=1)
    df['Group Status Change/FTE'] = df.apply(lambda x: x['Total Status Change Count']/x['FTE (Days)']  , axis=1)


    print(f"Adjudicated Case Count for 2018: {case_count:,}")
    print(f"Adjudicated Status Change Count for 2018: {status_change_count:,}" )
    print(f"Average Status Change Count/Case: {status_change_count/case_count : .2f}" )

    print(f"Adjudicated Cases/FTE Day: {case_count/FTE_DAYS_YEAR : .2f}")
    print(f"Status Changes/FTE Day: { status_change_count/FTE_DAYS_YEAR: .2f}")
#    print(f"Monthly Team Capacity (Status Changes) { (status_change_count/FTE_DAYS_YEAR) * FTE_DAYS_MONTH: ,.2f}" )


    ftedays_case_count = FTE_DAYS_YEAR/case_count
    ftedays_status_change_count = FTE_DAYS_YEAR/status_change_count
    print(f"FTE Days/Adjudicated Case: {ftedays_case_count : .3f}")
    print(f"FTE Days/Status Change {ftedays_status_change_count: .3f}")

    return (df, ftedays_case_count, ftedays_status_change_count )

# Internal Cell
def imgs_save(image):
    pass


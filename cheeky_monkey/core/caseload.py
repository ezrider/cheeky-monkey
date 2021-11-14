# AUTOGENERATED! DO NOT EDIT! File to edit: 02_core.caseload.ipynb (unless otherwise specified).

__all__ = ['CESSATION_CONTINUATION', 'get_generated_caseload_data_bymonth', 'get_processed_case_data',
           'f_caseload_isopen', 'build_range', 'filter_data', 'build_monthly_caseload', 'aggregate_monthly_data',
           'generate_caseload_data', 'generate_and_write_caseload_data']

# Cell
import pandas as pd
import numpy  as np
from datetime import datetime
import altair as alt

import random
import string

from pandas.util.testing import assert_frame_equal

pd.set_option('display.max_columns', 30) # set so can see all columns of the DataFrame

from vega_datasets import data
_=alt.data_transformers.disable_max_rows()


CESSATION_CONTINUATION = {
    'Driver Deceased': 'Deceased',
    'Drivers found medically unfit to drive':'Cessation',
    'Drivers that did not respond; cancelled license':'Cessation',
    'Drivers that voluntarily surrendered their license':'Cessation',
    'Drivers ultimately found fit to drive':'Continuation',
    'Cases remaining open at time of reporting':'Continuation'
}



# Cell
def get_generated_caseload_data_bymonth(f_path):
    filepath = f_path + 'caseloaddata_by_month.csv'
    caseload_data_by_month = pd.read_csv(filepath,parse_dates=['CASE_OPENED_DT'])
    caseload_data_by_month['Opened Month'] = caseload_data_by_month.apply(lambda x: x['CASE_OPENED_DT'].strftime('%b') + '-' + x['CASE_OPENED_DT'].strftime('%Y'), axis=1)

#    caseload_data_by_month['Opened Month'] = caseload_data_by_month.apply(lambda x: x['CASE_OPENED_DT'].strftime('%b') + '-' + x['CASE_OPENED_DT'].strftime('%Y'), axis=1)
    caseload_data_by_month['Monthly Opened Count'] = caseload_data_by_month.groupby(['CASE_OPENED_DT','Year Span'])['Open Count'].transform( lambda x: sum(x))
    caseload_data_by_month['Monthly Closed Count'] = caseload_data_by_month.groupby(['CASE_OPENED_DT','Year Span'])['Closed Count'].transform( lambda x: sum(x))

    return caseload_data_by_month



# Cell
def get_processed_case_data(f_path):
    file_path = f_path + 'cases_processed.csv'
    cases_df = pd.read_csv(file_path,parse_dates=['BIRTHDATE','CASE_OPENED_DT','PREV_CASE_END_DT','LAST_STATUS_DATE'], dtype={'DRIVERS_LICENSE_NO': str})
    cases_df = cases_df[(cases_df['Ignore Case'] == 0) ]
    cases_df['Age Category'] = cases_df.apply( lambda x: 'Over 80 ' if x.age_bucket >= 80 else 'Under 80', axis=1)
    cases_df['Type Origin'] = cases_df.apply( lambda x: str(x['CASE_CD']) + '_' + str(x['ORIGIN_CD']), axis=1)
    cases_df['Type & Origin Desc'] = cases_df.apply( lambda x: str(x['CASE_DSC']) + ' & ' + str(x['ORIGIN_DSC']), axis=1)
    cases_df['Case Length Over 30 Days'] = cases_df.apply( lambda x: True if x['case_length_days'] >= 30 else False, axis=1)
    cases_df['Case Length Over 60 Days'] = cases_df.apply( lambda x: True if x['case_length_days'] >= 60 else False, axis=1)
    return cases_df


# Cell
def f_caseload_isopen(r):
    # IS OPENED THIS MONTH
    if (r['Year Span'].month == r['CASE_OPENED_DT'].month):
        is_opened_this_month = 1
    else:
        is_opened_this_month = 0


    #check for valid 'last status date'
    testdate = pd.to_datetime(r['LAST_STATUS_DATE'], errors='ignore')

    if testdate is pd.NaT:
        status = 'Open'
        opened_count = is_opened_this_month
        closed_count = 0
        count_as_open = 1
        ignore_case = 0
        return (status, opened_count, closed_count, count_as_open, ignore_case, 99)


    try:
        testdate = pd.to_datetime(r['LAST_STATUS_DATE'])
    except ValueError:
        print('value error')
        status = 'Open'
        opened_count = 0
        closed_count = 0
        count_as_open = 1
        ignore_case = 0
        return (status, opened_count, closed_count, count_as_open, ignore_case, 99)
    except:
        print('generic error')
        status = 'Open'
        opened_count = 0
        closed_count = 0
        count_as_open = 1
        ignore_case = 0
        return (status, opened_count, closed_count, count_as_open, ignore_case, 100)



    # REPORT_OPEN_DIFF
    report_open_diff = r['Year Span'] - r['CASE_OPENED_DT'] # if same month then THIS IS OPENED MONTH
    report_open_diff = report_open_diff/np.timedelta64(1,'M')
    report_open_diff = int(report_open_diff)


    # IS CLOSE MONTH
    if (r['Year Span'].month == r['LAST_STATUS_DATE'].month):
        is_close_month = 1
    else:
        is_close_month = 0
    report_status_diff = r['Year Span'] - r['LAST_STATUS_DATE'] # if same month then
    report_status_diff = report_status_diff/np.timedelta64(1,'M')

    report_status_diff = int(report_status_diff)

    # REPORT
    status_diff = r['LAST_STATUS_DATE'] - r['CASE_OPENED_DT']
    status_diff = status_diff/np.timedelta64(1,'M')
    status_diff = int(status_diff)

    if 0:
        print('report_status_diff, is_close_month ', str(report_status_diff), ' ', str(is_close_month))
        print('report_open_diff, report_status_diff, statusdiff ', str(report_open_diff), ' ', str(report_status_diff), ' ',str(status_diff))

    if r['GENERAL_STATUS'] == 'Open':
        status = 'Open'
        # test to see if case opened this month
        if (report_open_diff == 0) :
            opened_count = 1
        else:
            opened_count = 0

        closed_count = 0
        count_as_open = 1
        ignore_case = 0

    else:
        # if ( ( ( report_open_diff <= 1) & ( report_open_diff > -1) ) & \
        #         ( ( report_status_diff < 1) & ( report_status_diff > -1) ) &  is_close_month ==1 ):  # test to see if the case both opened and closed this month:  # test to see if the case closed this month
        if  ( ( report_open_diff <= 1) & ( report_open_diff > -1) ) and \
                ( ( report_status_diff < 1) & ( report_status_diff > -1) ) and ( is_close_month ==1 ):  # test to see if the case both opened and closed this month:  # test to see if the case closed this month
            status = 'Closed'
            opened_count = is_opened_this_month
            closed_count = 1
            count_as_open = 0
            ignore_case = 0
        elif ( ( ( report_open_diff < 1) & ( report_open_diff > -1) ) and \
                ( ( report_status_diff < 1) & ( report_status_diff > -1) ) and  is_close_month == 0 ):  # test to see if the case both opened and closed this month:  # test to see if the case closed this month
            status = 'Open'
            opened_count = is_opened_this_month
            closed_count = 0
            count_as_open = 1
            ignore_case = 0

        elif ( ( report_open_diff < 1) and ( report_open_diff > -1) )  :#& ( ( year_span_diff < 1) & ( year_span_diff > -1) ):  # test to see if the case closed this month
            status = 'Open'
            opened_count = 1
            closed_count = 0
            count_as_open = 1
            ignore_case = 0
        elif report_status_diff < 0  :
            status = 'Open'
            opened_count = 1
            closed_count = 0
            count_as_open = 1
            ignore_case = 0
        elif ( ( report_status_diff < 1) and ( report_status_diff > -1) ):  # test to see if the case closed this month
            status = 'Closed'
            opened_count = 0
            closed_count = is_close_month
            if is_close_month:
                count_as_open = 0
            else:
                count_as_open = 1
            ignore_case = 0
        else:
            status = 'Closed'
            opened_count = 0
            closed_count = 0
            count_as_open = 0
            ignore_case = 1


    return (status, opened_count, closed_count, count_as_open, ignore_case, report_open_diff)


# Cell
def build_range():
    #r = pd.date_range(*(pd.to_datetime([datetime.strptime('1-1-2018', '%d-%m-%Y'), datetime.strptime('1-9-2021', '%d-%m-%Y')]) + pd.offsets.MonthEnd()), freq='M')
    r = pd.date_range(*(pd.to_datetime([datetime.strptime('1-1-2018', '%d-%m-%Y'), datetime.strptime('1-11-2021', '%d-%m-%Y')]) + pd.offsets.MonthEnd()), freq='M')
    return r


# Cell
def filter_data(d, year, month):
    return d[(d.opened_year == year) & ( d.opened_month == month )].reset_index()


# Cell

#export
def build_monthly_caseload(d, end_date, filename=None):
    """given a dataframe, and an enddate for the period, return a dataframe with a case 'status info' record for each month

    Parameters:
    dataframe (pd.DataFrame):
    end_date (datetime): date to limit the generation of case 'status info' records
    filename (str): <todo>

    Returns:
    pd.DataFrame

   """
    #data = d[d['LAST_STATUS_DATE'].notna()].reset_index()

    data = d
    data['Year Date'] = end_date

    data['Year Span'] = [pd.date_range(*(pd.to_datetime([s, e]) + pd.offsets.MonthEnd()), freq='M') for s, e in
                  zip(pd.to_datetime(data['CASE_OPENED_DT']),
                       pd.to_datetime(data['Year Date']))]

    data = data.explode('Year Span')

    if data.empty:
        return None

    # changing to f_caseload to return (status, opened_count, closed_count, count_as_open, open_year_span_diff)

    data[['Status', 'Opened Count', 'Closed Count', 'Count as Open', 'Ignore Case',  'open_year_span_diff']] = data.apply( f_caseload_isopen   , axis=1).to_list()

    if filename:
        summaryfilename = filename.replace('.csv', '_Adjudicated_Summary.csv' ) #Jan_2018_toSept2021.csv

        print(filename)
        #data.to_csv(filename, index = False)

    data = data[data['Ignore Case'] == 0].reset_index(drop=True)

    return data



# Cell

#export
def aggregate_monthly_data(data, ag_dict={}):
    """given a dataframe, and an enddate for the period, return a dataframe with a case 'status info' record for each month

    Parameters:
    data (pd.DataFrame):
    by (list): list of fields to group by

    Returns:
    pd.DataFrame

    """
    # we have determined impact for each case, now aggregate numbers so we have the impact for the month of data
    if len(ag_dict.keys()) > 0:
        aggregation = ag_dict
    else:
        aggregation = {
        'Opened Count': ('Opened Count','sum'),
        'Count as Open': ('Count as Open','sum'),
        'Closed': ('Closed Count','sum')
        # 'Case Count': ('DRIVERS_LICENSE_NO','count'),
        #     'Status Count': ('STATUS_COUNT', 'sum')
        }

    monthly_counts = data.groupby([pd.Grouper(freq='M', key='CASE_OPENED_DT') ,
                                  pd.Grouper(key='Year Span'),
                                  pd.Grouper(key='Status'),
                                  pd.Grouper(key='Age Category'),
                                 ]).agg(** aggregation)

    monthly_counts = pd.DataFrame(monthly_counts).reset_index()
    #monthly_counts.to_csv(summaryfilename, index = False)

    return monthly_counts

# Cell
def generate_caseload_data(dataframe):
    """process the case data month-by=month

    Parameters:
    dataframe (pd.DataFrame)
    f_path (str): the file path wher the generated caseload data should be put

    Returns:
    pd.DataFrame

    """

    caseload_data = pd.DataFrame()

    r = build_range()
    #for date in r[:2]:
    for date in r:

        if (date.year == r[-1].year) and (date.month == r[-1].month) : break

        #filename = generated_data_file_path + date.strftime("%b") + '_' + date.strftime("%Y") + '_' + 'toNov2021_ADJUDICATEDCASELOAD' + '.csv'

        monthly_data = filter_data(dataframe, date.year, date.month)

        caseload_month = build_monthly_caseload(monthly_data,r[-1])  # call func without file path so the intermediate files don't get writtn

        #caseload_month = build_monthly_caseload(monthly_data,r[-1], filename)

        if caseload_month is None:
            break
        if caseload_data.empty:
            caseload_data = caseload_month
        else:
            caseload_data = caseload_data.append(caseload_month)

    return caseload_data



# Cell
def generate_and_write_caseload_data(dataframe, f_path):
    """process the case data month-by=month

    Parameters:
    dataframe (pd.DataFrame)
    f_path (str): the file path wher the generated caseload data should be put

    Returns:
    pd.DataFrame

    """
    filename = f_path + 'caseloaddata_by_month.csv'
    caseload_data = generate_caseload_data(dataframe)
    caseload_summary = aggregate_monthly_data(caseload_data)
    caseload_summary.to_csv(filename, index = False)
    return caseload_summary
    # caseload_data.to_csv(filename, index = False)
    # return caseload_data

import pandas as pd
import numpy as np
import math
import os
import datetime
import matplotlib as plt
from sklearn import preprocessing
pd.set_option('display.max_columns', 200)

trans_train = pd.read_csv("./data/trans_train.csv",na_values= ['?', 'NA', ''],sep=  ';')
card
def clean_transaction(filename):
    trans = pd.read_csv(filename,na_values= ['?', 'NA', ''],sep=  ';')
 #   trans.loc[trans["operation"].isna(),"operation"] = trans.loc[trans["operation"].isna(),"k_symbol"]
    trans.loc[trans["type"]=="withdrawal in cash","type"] = "withdrawal"
    trans.loc[trans["type"]=="withdrawal","amount"] *=-1 
 #   trans = trans.drop(['k_symbol'], axis=1)
    trans = trans.drop(['bank', 'account'], axis=1)
 #   trans["date"] = pd.to_datetime(trans['date'], format='%y%m%d')

    #group balances of the same account and get avg, min and max values of balance
    grouped_balance = trans.sort_values(by=['account_id', 'date'],
                                            ascending=[True, False]).groupby(['account_id']).agg({'balance': ['mean', 'max', 'min','std']}).reset_index()
    grouped_balance.columns = ['account_id', 'balance_mean', 'balance_max', 'balance_min', 'balance_std']
    grouped_balance['reached_negative_balance'] = grouped_balance['balance_min']
    grouped_balance.loc[grouped_balance["balance_min"] >= 0, "reached_negative_balance"] = 0
    grouped_balance.loc[grouped_balance["balance_min"] < 0, "reached_negative_balance"] = 1

   # 
    aux_types = trans.sort_values(by=['account_id', 'date'],ascending=[True, False]).groupby(['account_id', 'type']).agg({'amount': ['mean', 'count', 'max', 'min']}).reset_index()
    aux_types.columns = ['account_id', 'type', 'type_mean', 'type_count','type_max', 'type_min']

    grouped_credits = aux_types[aux_types['type'] == 'credit']
    grouped_credits.columns = ['account_id', 'type', 'credit_mean', 'credit_count','credit_max', 'credit_min']
    grouped_credits.drop(['type'], axis=1)
    
    grouped_withdrawals = aux_types[aux_types['type'] == 'withdrawal']
    grouped_withdrawals.columns = ['account_id', 'type', 'withdrawal_mean', 'withdrawal_count', 'withdrawal_max', 'withdrawal_min']
    grouped_withdrawals.drop(['type'], axis=1)


    group_k_symbol = trans.groupby(['account_id', 'k_symbol']).agg({'amount': ['mean', 'sum', 'count']}).reset_index()
    group_k_symbol.columns = ['account_id', 'k_symbol', 'amount_mean','amount_sum', 'amount_count']

      # extract households stats
    households = group_k_symbol[group_k_symbol['k_symbol'] == 'household']
    households.columns = ['account_id', 'k_symbol', 'household_mean', 'household_sum', 'household_count']
    households = households.drop(['k_symbol'], axis=1)
    
    # extract pensions stats
    pensions = group_k_symbol[group_k_symbol['k_symbol'] == 'old-age pension']
    pensions.columns = ['account_id', 'k_symbol', 'pension_mean', 'pension_sum', 'pension_count']
    pensions = pensions.drop(['k_symbol'], axis=1)
    
    # extract sanction payment stats
    sanctions = group_k_symbol[group_k_symbol['k_symbol'] == 'sanction interest if negative balance']
    sanctions.columns = ['account_id', 'k_symbol', 'sanctions_mean', 'sanctions_sum',
                        'sanctions_count']
    sanctions = sanctions.drop(['k_symbol'], axis=1)

    # extract payments for statement stats
    payment_st = group_k_symbol[group_k_symbol['k_symbol'] == 'payment for statement']
    payment_st.columns = ['account_id', 'k_symbol', 'payment_statement_mean', 'payment_statement_sum',
                        'payment_statement_count']
    payment_st = payment_st.drop(['k_symbol'], axis=1)
    
    # extract insurance payment stats
    insurances = group_k_symbol[group_k_symbol['k_symbol'] == 'insurrance payment']
    insurances.columns = ['account_id', 'k_symbol', 'insurances_mean', 'insurances_sum',
                        'insurances_count']
    insurances = insurances.drop(['k_symbol'], axis=1)

    processed_trans = grouped_balance.merge(grouped_credits, on='account_id', how='left')\
                     .merge(grouped_withdrawals, on='account_id', how='left')\
                     .merge(households, on='account_id', how='left')\
                     .merge(pensions, on='account_id', how='left')\
                     .merge(payment_st, on='account_id', how='left')\
                     .merge(insurances, on='account_id', how='left')\
                     .merge(sanctions, on='account_id', how='left')
    processed_trans=processed_trans.fillna(0)
    processed_trans.to_csv("pt.csv")
    


    return processed_trans


trans_train=clean_transaction("./data/trans_train.csv")

def build_account_disp_card(card):
   

clean_account()
#!/usr/bin/python
def get_search_service_base_url():
    return 'http://localhost:9200/finance/_search?pretty'
def get_recommend_service_base_url():
    return "http://localhost:5200/recommend?"
#def get_adverse_service_base_url():
#    return "http://jinrongdao.com:8081/adverse/matched_adverse?"
def get_search_service_classify_url():
    return 'http://localhost:9200/finance/_search?pretty'

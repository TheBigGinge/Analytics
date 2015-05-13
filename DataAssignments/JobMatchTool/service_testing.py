import RequestService.elasticsearch_requests as er
import RequestService.ranking_service as rs


er.ElasticRequest('accounting assistant', 'public administration',
                  "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\OutData\\").job_results_to_tsv_location()

rs.RankingService("\\\\filer01\\public\\Data_Analytics\\JobMatcher\\OutData\\input.tsv",
                  "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\OutData\\").rank_request()
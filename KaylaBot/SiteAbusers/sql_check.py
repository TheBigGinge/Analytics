import SqlTools.payscale_replicated as pr

data = pr.SqlServer("SiteStats")

query = '''
declare     @StartDate datetime
declare     @EndDate datetime
declare     @pageName varchar(255)
declare     @codeName varchar(255)
declare     @codeVal varchar(255)

set @StartDate = '{0}'
set @EndDate = '{1}'
set @pageName = '/mypayscale.aspx'
set @codeName = 'ProfileGuid'


-- logtoken token_types: VISITOR, IPADDR, CODENAME, CODEVAL, PAGENAME, USERAGNT, REFERER

-- get unique profiles viewed on my payscale

select lt.token_value as ip_address, count(distinct plf.code_value_id) as cnt
from ProcessedLogFiles plf with  (nolock)
inner join LogTokens lt on lt.token_id = plf.ip_address
where
      plf.date_created < @EndDate and plf.date_created > @StartDate and
      plf.PAGE_NAME_ID = (select token_id FROM LogTokens WHERE Token_type = 'PAGENAME' AND token_value_for_index = @pageName) and
      plf.code_name_id = (select token_id FROM LogTokens WHERE Token_type = 'CODENAME' AND token_value_for_index = @codeName)
group by lt.token_value order by cnt desc
'''.format('2014-07-01', '2014-07-31')

data.set_query_string(query)

data.initialize_connection()

for row in data.return_results():
    print row.ip_address, row.cnt
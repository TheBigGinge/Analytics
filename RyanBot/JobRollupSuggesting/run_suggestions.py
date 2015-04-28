import unprompted as un
import suggestion_helper as support
import suggest as rollups


create_unprompted = un.CreateUnpromptedStrings()
create_unprompted.gather_data()
create_unprompted.create_dictionaries()
create_unprompted.create_unprompted_file()
unprompted_files = create_unprompted.current_unprompted

jobs_without_rollups = support.SuggestionHelper().pull_jobs_no_rollups()
support.SuggestionHelper().run_analysis_tool()
job_eac_dict = support.SuggestionHelper().extract_data()

rollups.SuggestRollups(unprompted_files, job_eac_dict, jobs_without_rollups)
rollups.JobEACDifference(job_eac_dict)



mkdir datasets
cd datasets
aws s3 cp s3://navi-tech-journey/2021-hackathon-esg/data/companies_br.csv companies_br.csv
aws s3 cp s3://navi-tech-journey/2021-hackathon-esg/data/companies_financials_br.csv companies_financials_br.csv
aws s3 cp s3://navi-tech-journey/2021-hackathon-esg/data/esg_scores_history_br.csv esg_scores_history_br.csv
aws s3 cp s3://navi-tech-journey/2021-hackathon-esg/data/environmental_data_history_br.csv environmental_data_history_br.csv

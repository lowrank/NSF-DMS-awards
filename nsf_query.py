
import os
import requests
import pandas as pd
import json


program_elements_codes = {
    "Algebra and Number Theory": "1264",
    "Analysis": "1281",
    "Applied Mathematics": "1266",
    "Combinatorics": "7970",
    "Computational Mathematics": "1271",
    "Foundations": "1268",
    "Geometric Analysis": "1265",
    "Mathematical Biology": "7334",
    "Probability": "1263",
    "Statistics": "1269",
    "Topology": "1267"
}

def generate_query_url(program_name, start_year):
    """Generate NSF API query URL for awards in a given year."""
    base_url = 'https://api.nsf.gov/services/v1/awards.json'
    params = {
        'ProgEleCode': program_elements_codes[program_name],
        'BooleanElement': 'All',
        'ActiveAwards': 'true',
        'ExpiredAwards': 'true',
        'StartDateFrom': f'01/01/{start_year}',
        'StartDateTo': f'12/31/{start_year}',
        'StartDateOperator': 'Range',
        'org_code_div': '03040000',
        'rpp': '3000',
        'offset': '0',
        'sortKey': 'startDate'
    }
    
    # Build URL with query parameters
    url = base_url + '?'
    url += '&'.join([f'{k}={v}' for k, v in params.items()])
    return url


def get_awards_csv(program_name, year):
    """Fetch awards from NSF API and save as CSV."""
    
    url = generate_query_url(program_name, year)
    print(f"Fetching: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract awards from response
        if 'response' in data and 'award' in data['response']:
            awards = data['response']['award']
            df = pd.json_normalize(awards)
            
            # Combine first and last name for PrincipalInvestigator
            if 'piFirstName' in df.columns and 'piLastName' in df.columns:
                df['PrincipalInvestigator'] = df['piFirstName'].fillna('') + ' ' + df['piLastName'].fillna('')
                df['PrincipalInvestigator'] = df['PrincipalInvestigator'].str.strip()
            
            # Map API column names to desired column names
            column_mapping = {
                'id': 'AwardNumber',
                'title': 'Title',
                'orgLongName': 'NSFOrganization',
                'program': 'Program(s)',
                'startDate': 'StartDate',
                'latestAmendmentDate': 'LastAmendmentDate',
                'PrincipalInvestigator': 'PrincipalInvestigator',
                'awardeeStateCode': 'State',
                'awardeeName': 'Organization',
                'transType': 'AwardInstrument',
                'poName': 'ProgramManager',
                'expDate': 'EndDate',
                'estimatedTotalAmt': 'AwardedAmountToDate',
                'coPDPI': 'Co-PIName(s)',
                'piEmail': 'PIEmailAddress',
                'awardeeAddress': 'OrganizationStreet',
                'awardeeCity': 'OrganizationCity',
                'awardeeZipCode': 'OrganizationZip',
                'awardeePhone': 'OrganizationPhone',
                'dirAbbr': 'NSFDirectorate',
                'progEleCode': 'ProgramElementCode(s)',
                'progRefCode': 'ProgramReferenceCode(s)',
                'fundsObligatedAmt': 'ARRAAmount',
                'abstractText': 'Abstract'
            }
            
            # Select and rename columns that exist
            existing_mapping = {k: v for k, v in column_mapping.items() if k in df.columns}
            df = df[list(existing_mapping.keys())].rename(columns=existing_mapping)
            
            # Define the final column order
            final_columns = [
                'AwardNumber', 'Title', 'NSFOrganization', 'Program(s)',
                'StartDate', 'LastAmendmentDate', 'PrincipalInvestigator', 'State',
                'Organization', 'AwardInstrument', 'ProgramManager', 'EndDate',
                'AwardedAmountToDate', 'Co-PIName(s)', 'PIEmailAddress', 'OrganizationStreet',
                'OrganizationCity', 'OrganizationZip', 'OrganizationPhone',
                'NSFDirectorate', 'ProgramElementCode(s)', 'ProgramReferenceCode(s)', 'ARRAAmount', 'Abstract'
            ]
            
            # Reorder columns, keeping only those that exist
            existing_final_columns = [col for col in final_columns if col in df.columns]
            df = df[existing_final_columns]
        else:
            print(f"No awards found for {program_name} {year}")
            return 2
        
        # Create directory if needed
        cur_dir = os.path.dirname(__file__)
        prog_dir = program_name.replace(" ", "-")
        
        if not os.path.isdir(os.path.join(cur_dir, prog_dir)):
            os.mkdir(os.path.join(cur_dir, prog_dir))
        
        # Save to CSV
        target_file = os.path.join(os.path.join(cur_dir, prog_dir), "Awards-" + program_name.replace(" ", "-") +"-" + str(year) + ".csv")
        
        # Check if file already exists
        if os.path.exists(target_file):
            try:
                try:
                    old_df = pd.read_csv(target_file, encoding='latin-1')
                except:
                    old_df = pd.read_csv(target_file, encoding='utf-8')
                old_num_rows = len(old_df)
            except:
                # File exists but is empty or unreadable
                old_num_rows = 0
            
            new_num_rows = len(df)
            
            print(f"File exists with {old_num_rows} rows. New data has {new_num_rows} rows.")
            
            if new_num_rows > old_num_rows:
                df.to_csv(target_file, index=False)
                print(f"Replaced {target_file} with newer data")
                return 0
            else:
                print(f"New data does not have more rows. Keeping existing file.")
                return 1
        
        # Save the dataframe to CSV
        df.to_csv(target_file, index=False)
        print(f"Saved awards to: {target_file}")
        return 0
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {program_name} {year}: {e}")
        return 3


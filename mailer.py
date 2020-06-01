from airtable import Airtable
import markdown2 as md


def get_emails():
    airtable=Airtable('app31EjwB2Plb9dBV','List')
    get_emails = airtable.get_all(fields='Email')
    #print(f'{get_emails}"\n"{len(get_emails)}')
    ps=[]
    for i in range(len(get_emails)):
        ps.append(get_emails[i].get('fields').get('Email'))
    return ps

def render_markdown(file):
    return md.markdown(file.read())

def
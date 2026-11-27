def catalog_checks(data):
    return [{'url':x['url'],'issues':(['missing title'] if not x.get('title') else [])+(['empty listing'] if x.get('item_count')==0 else [])} for x in data]

def media_checks(data):
    return [{'url':x['url'],'issues':(['missing alt'] if x['type']=='image' and not x.get('decorative') and not x.get('alt') else [])+(['missing transcript'] if x['type']=='video' and not x.get('transcript') else [])} for x in data]

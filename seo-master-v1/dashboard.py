import argparse,json,secrets
import live_research
import strategy
import execution
import delivery
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from workspace import Workspace
from offline import METHODS
ROOT=Path(__file__).resolve().parent

def server(workspace,port=8765):
    token=secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def reply(self,status,data,kind='application/json'):
            body=json.dumps(data,allow_nan=False).encode() if kind=='application/json' else data.encode()
            self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'");self.end_headers();self.wfile.write(body)
        def valid(self):return self.headers.get('Host')==f'127.0.0.1:{self.server.server_port}'
        def do_GET(self):
            if not self.valid():return self.reply(403,{'error':'Invalid host'})
            if self.path=='/':return self.reply(200,(ROOT/'ui/index.html').read_text().replace('__TOKEN__',token),'text/html')
            if self.path in ('/app.js','/style.css'):return self.reply(200,(ROOT/'ui'/self.path[1:]).read_text(),'text/javascript' if self.path.endswith('js') else 'text/css')
            if self.path.startswith('/api/package/'):
                try: body=delivery.package(workspace.export(self.path.split('/')[-1]))
                except ValueError:return self.reply(404,{'error':'Unknown project or invalid data'})
                self.send_response(200);self.send_header('Content-Type','application/zip');self.send_header('Content-Disposition','attachment; filename=seo-research.zip');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
            if self.path=='/api/projects':return self.reply(200,workspace.projects())
            if self.path=='/api/providers':return self.reply(200,execution.provider_status())
            if self.path=='/api/methods':return self.reply(200,sorted(METHODS))
            if self.path.startswith('/api/export/'):
                try:return self.reply(200,workspace.export(self.path.split('/')[-1]))
                except ValueError:return self.reply(404,{'error':'Unknown project'})
            self.reply(404,{'error':'Not found'})
        def do_POST(self):
            if not self.valid() or self.headers.get('X-Workspace-Token')!=token:return self.reply(403,{'error':'Forbidden'})
            try:
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<=2_000_000:raise ValueError('Invalid request size')
                d=json.loads(self.rfile.read(n))
                if self.path=='/api/projects':return self.reply(201,{'id':workspace.create(d)})
                if self.path=='/api/page':return self.reply(200,delivery.save_page(workspace,d['project'],d))
                if self.path=='/api/opportunity':return self.reply(200,delivery.save_opportunity(workspace,d['project'],d))
                if self.path=='/api/delivery':return self.reply(200,delivery.build(workspace.export(d['project'])))
                if self.path=='/api/provider':return self.reply(200,execution.collect(workspace,d['project'],d))
                if self.path=='/api/execute':return self.reply(200,execution.execute(workspace,d['project'],d['tasks']))
                if self.path=='/api/research':
                    key=d['project']; project=workspace.export(key)['project']; kind=d['kind']
                    if kind in ('competitors','crawl') and d.get('authorized') is not True:raise ValueError('Network authorization required')
                    if kind=='competitors':rows=live_research.discover(d['query'],project.get('domain',''))
                    elif kind=='crawl':rows=live_research.crawl(d['url'],d['limit'])
                    elif kind=='keywords':rows=live_research.keyword_rows(d['csv'],d['market'],d['language'],d['source'])
                    elif kind in ('content_map','ai_observations','backlinks'):rows=strategy.records(kind,d)
                    else:raise ValueError('Unknown research type')
                    return self.reply(200,workspace.save_records(key,kind,rows))
                if self.path=='/api/strategy':
                    r=workspace.export(d['project'])['research']
                    return self.reply(200,{'technical':strategy.technical(r['crawl']),'content':strategy.content(r['keywords'],r['content_map']),'visibility':strategy.visibility(r['ai_observations']),'authority':strategy.backlinks(r['backlinks'])})
                if self.path=='/api/run':return self.reply(200,workspace.run(d['project'],d['method'],d['payload']))
                return self.reply(404,{'error':'Not found'})
            except ValueError as e:return self.reply(400,{'error':str(e)})
            except (KeyError,TypeError,ArithmeticError,OSError,RuntimeError):return self.reply(400,{'error':'Research request failed; check inputs, connection and credentials'})
    return HTTPServer(('127.0.0.1',port),Handler)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--db',default='workspace.sqlite');p.add_argument('--port',type=int,default=8765);a=p.parse_args();s=server(Workspace(a.db),a.port);print(f'Open http://127.0.0.1:{s.server_port}',flush=True);s.serve_forever()

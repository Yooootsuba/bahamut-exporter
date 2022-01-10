
from urllib.parse import urlparse, parse_qs
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from ..core.service import BamahutExporterService

VERSION_BANNER = """
Exports floors and replies in Bahamut posts %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Exports floors and replies in Bahamut posts'

        # text displayed at the bottom of --help output
        epilog = 'Usage: bahamutexporter -u URL'

        # controller level arguments. ex: 'bahamutexporter --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
            ( [ '-u', '--url' ],
              { 'action'  : 'store',
                'dest' : 'url' } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        if self.app.pargs.url is None:
            self.app.args.print_help()
        else:
            service = BamahutExporterService()
            queries = parse_qs(urlparse(self.app.pargs.url).query)
            floors  = {'floors': service.export(queries['bsn'][0], queries['snA'][0])}
            self.app.render(floors, 'html.jinja2')

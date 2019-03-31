import requests
import upt
 
class NpmPackage(upt.Package):
    pass


class NpmFrontend(upt.Frontend):
    name = 'npm'
    def get_archives(self, version):
        dist = version['dist']
        url = dist.get('tarball')
        archive = upt.Archive(url)
        return [archive]

    def parse(self, pkg_name):
        url = f'https://registry.npmjs.org/{pkg_name}'
        r = requests.get(url)
        if not r.ok:
            raise upt.InvalidPackageNameError(self.name, pkg_name)
        self.json = r.json()
        
        version = self.json['dist-tags']['latest']
        archive = self.get_archives(self.json['versions'][version])
        
        pkg_args = {
            # 'summary': self.json['readme'],
            'homepage': self.json['homepage'],
            'download_urls': self.json['repository']['url'],
            'summary': self.json['description'],
            'licenses': self.json['license'],
            'archives': archive,
        }
        
        return NpmPackage(pkg_name, version, **pkg_args)

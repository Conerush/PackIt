from tinydb import TinyDB, Query
db = TinyDB('packages_db.json')
import json 

packages_table = db.table('packages')
Package = Query()

# Load in data
with open('formatted_package_version.json', 'r') as json_file:
    data = json.load(json_file)


packages = []
for key in data:
    for version in data[key]:
        value = {'package_name':key, 'python_version':version, 'package_version': data[key][version]}
        packages.append(value)

for i in packages:
    packages_table.insert(i)

def get_package_version(package_name, python_version):
    result = packages_table.get((Package.package_name == package_name) & (Package.python_version == python_version))
    if result:
        return result['package_version']
    else:
        return None
    

package_name = 'pygments'
python_version = 'Python 3.8'
package_version = get_package_version(package_name, python_version)
print(f'The version {package_name} for Python {python_version} is {package_version}')
print(packages_table.all())
import os

home = os.listdir()

for home_dir in home:
	if os.path.isdir(home_dir):
		for app_folder in os.listdir(home_dir):
			# print(app_folder)
			if app_folder == 'migrations':
				path = os.path.join(home_dir, app_folder)
				for item in os.listdir(path):

					if item[0] == '0':

						os.remove(os.path.join(path, item))
			
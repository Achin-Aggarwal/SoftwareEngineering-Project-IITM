from Application import app, api, jwt


# print("Registered routes:")
# for rule in app.url_map.iter_rules():
#     print(rule)

if __name__ == '__main__':
   app.run(debug=True,use_reloader=False)
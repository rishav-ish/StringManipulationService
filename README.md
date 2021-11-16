# StringManipulationService
Basic REST Flask API that add string to database and can also perform some basic operation like reverse, flip, etc

## API DOCUMENTATION

- GET: /api/v1/strings -> Return all the string stored in database and there ids
- POST: /api/v1/strings -> Take {name:val} and stored the string name and returns its id
- GET: /api/v1/string/operation/{id} -> Take id and return all the operations perform on that id string
- POST: /api/v1/string/operation -> Take{id:id, operation:operation_name} and perform the operation and store the new string generated and return its id



App is deployed https://stringmanipulationapi.com/

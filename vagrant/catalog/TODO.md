# Primary Requirements

* Finalize SEF url format / API
* Basic CRUD
* Latest items displayed on landing page - name/category
  * ~~Display based on last modified date aka most recent~~
  * Add item count to each category
  * Add category membership to item listing
* Display selected categories items alongside categories
* ~~Detail page on an Item~~
  * clean up and format
* Delete confirmation page for category
* ~~Edit item page~~
  * clean up and format
  * add category changing / copying
* sanitize HTML in user entered strings
* OAuth login
* JSON REST API
  * overload http routes to use JSON
* ERRORS:
  * handle sqlalchemy.exc.IntegrityError when adding duplicate items
  * handle sqlalchemy.exc.InvalidRequestError after an IntegrityError - needs session.rollback()
Bonus:
* upload/add image to item or category
* extra comments on items/categories
* add nonce's to delete POST - https://clipperz.is/security_privacy/crypto_algorithms/

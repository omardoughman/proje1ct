from flask import Flask, request, jsonify, Response
import sqlite3
import time

app = Flask(__name__)

DB = "odata.db"

# ---------------------------
# DB
# ---------------------------

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init():
    conn = db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Email TEXT,
        Role TEXT,
        CreatedAt INTEGER
    )
    """)

    # seed data
    c.execute("INSERT OR IGNORE INTO Users (Id, Name, Email, Role, CreatedAt) VALUES (1, 'Admin', 'admin@local', 'admin', ?)",
              (int(time.time()),))

    conn.commit()
    conn.close()

init()

# ---------------------------
# ODATA SERVICE ROOT (like service.odata.org)
# ---------------------------

@app.route("/odata/")
def service_root():
    return jsonify({
        "@odata.context": "/odata/$metadata",
        "value": [
            {
                "name": "Users",
                "kind": "EntitySet",
                "url": "Users"
            }
        ]
    })


# ---------------------------
# METADATA (simplified EDMX-like XML)
# ---------------------------

@app.route("/odata/$metadata")
def metadata():
    xml = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0"
 xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">

 <edmx:DataServices>
  <Schema Namespace="Demo" xmlns="http://docs.oasis-open.org/odata/ns/edm">

   <EntityType Name="User">
    <Key><PropertyRef Name="Id"/></Key>
    <Property Name="Id" Type="Edm.Int32"/>
    <Property Name="Name" Type="Edm.String"/>
    <Property Name="Email" Type="Edm.String"/>
    <Property Name="Role" Type="Edm.String"/>
    <Property Name="CreatedAt" Type="Edm.Int64"/>
   </EntityType>

   <EntityContainer Name="Default">
    <EntitySet Name="Users" EntityType="Demo.User"/>
   </EntityContainer>

  </Schema>
 </edmx:DataServices>
</edmx:Edmx>
"""
    return Response(xml, mimetype="application/xml")


# ---------------------------
# ENTITY SET: /Users
# ---------------------------

@app.route("/odata/Users")
def users():

    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM Users")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    # ---- simple OData query support ----
    top = request.args.get("$top")
    select = request.args.get("$select")

    if top and top.isdigit():
        rows = rows[:int(top)]

    if select:
        fields = select.split(",")
        rows = [
            {k: r[k] for k in fields if k in r}
            for r in rows
        ]

    return jsonify({
        "@odata.context": "/odata/$metadata#Users",
        "value": rows
    })


# ---------------------------
# RUN SERVER
# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)

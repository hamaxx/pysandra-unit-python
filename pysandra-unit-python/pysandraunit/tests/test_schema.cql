CREATE KEYSPACE testks
 WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 1} ;

USE testks ;

CREATE TABLE ascii (
  key text,
  column1 text,
  value text,
  PRIMARY KEY (key, column1)
 ) WITH COMPACT STORAGE ;

CREATE TABLE ascii_counter (
  key text,
  column1 text,
  value counter,
  PRIMARY KEY (key, column1)
 ) WITH COMPACT STORAGE ;

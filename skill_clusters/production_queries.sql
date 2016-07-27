# Number of positions by company
SELECT c.name, count(c.name)
FROM companies c
INNER JOIN open_positions o
ON c.id = o.company_id
GROUP BY c.name
;

# Total number of positions
SELECT count(*)
FROM open_positions
;

# Total number of positions for company_id "6"
SELECT count(*)
FROM open_positions
WHERE company_id = 6
;

# Trends for "Oracle Developer" job
SELECT t.name, pi.score
FROM trends t
INNER JOIN position_inputs pi
ON t.id = pi.trend_id
INNER JOIN open_positions op
ON pi.open_position_id = op.id
WHERE op.id = 28
;

# Trends by applicant for Thumbtack (limit 10000 values)
SELECT a.id, a.first_name, a.last_name, at.trend_id, t.name, t.kind
FROM applicants a
INNER JOIN applicant_trends at
ON a.id = at.applicant_id
INNER JOIN trends t
ON at.trend_id = t.id
WHERE a.company_id = 8
LIMIT 10000
;

# Get trends for one applicant
SELECT a.id, a.first_name, a.last_name, at.trend_id, t.name, t.kind
FROM applicants a
INNER JOIN applicant_trends at
ON a.id = at.applicant_id
INNER JOIN trends t
ON at.trend_id = t.id
WHERE a.id = 531968
;

# Get names for specific trend "kind"
SELECT a.id, a.first_name, a.last_name, at.trend_id, t.name, t.kind
FROM applicants a
INNER JOIN applicant_trends at
ON a.id = at.applicant_id
INNER JOIN trends t
ON at.trend_id = t.id
WHERE t.kind = 'Communication'
LIMIT 500
;

# Get names for list of trend "kind"
SELECT a.id, a.first_name, a.last_name, at.trend_id, t.name, t.kind
FROM applicants a
INNER JOIN applicant_trends at
ON a.id = at.applicant_id
INNER JOIN trends t
ON at.trend_id = t.id
WHERE t.kind IN (
    'Awards',
    'Brands',
    'Communication',
    'Custom',
    'FieldTerminology',
    'JobTitle',
    'OperatingSystem',
    'ProfessionalDegree',
    'Skill Cluster',
    'Software systems',
    'Technology')
;

-- # "kinds" to keep
-- Awards
-- Brands
-- Communication
-- Custom
-- FieldTerminology
-- JobTitle
-- OperatingSystem
-- ProfessionalDegree
-- Skill Cluster
-- Software systems
-- Technology

-- # "kinds" to remove
-- Animal
-- Agencies
-- Anatomy
-- Artifacts
-- Associations & groups
-- Automobile
-- Character
-- City
-- Communication system
-- Companies
-- Company
-- Consumer products
-- Continent
-- Continents
-- Countries
-- Country
-- Crime
-- custom
-- Degree
-- Diseases
-- Drug
-- EmailAddress
-- Empires
-- EntertainmentAward
-- Events
-- Facility
-- FinancialMarketIndex
-- Food
-- GeographicFeature
-- Hardware and gadgets
-- Hashtag
-- HealthCondition
-- Historic events
-- Holiday
-- IPAddress
-- Laws
-- Locations & natural formations
-- Medicines
-- Movie
-- MusicGroup
-- NaturalDisaster
-- Natural events
-- Organization
-- Organizations
-- OTHERS
-- Outlets
-- People
-- Periods
-- Person
-- Plant
-- Political events
-- Political group
-- PrintMedia
-- Product
-- Projects
-- Publication
-- Quantity
-- Region
-- Religion
-- Religious figure
-- Scale/unit
-- Show
-- Sport
-- SportingEvent
-- StateOrCounty
-- Stock market
-- Substance
-- Teams
-- TelevisionShow
-- TelevisionStation
-- Tournaments
-- TwitterHandle
-- Weaponry
-- Zodiac sign
-- NULL

# Distinct "kind" values from the Trends table - 86 total
SELECT DISTINCT(kind)
FROM trends
ORDER BY 1
;

# Count of trends for engineering roles at Thumbtack
SELECT COUNT(1), t.name
FROM trends t, applicant_trends at, applicants a
WHERE t.id = at.trend_id
AND a.id = at.applicant_id
AND a.company_id = 8
AND ARRAY['engineer', 'engineering'] @> a.roles
GROUP BY t.name
ORDER BY 2
;

# Leads for 3 positions at Thumbtack
SELECT * FROM leads WHERE position_id IN(188, 190, 192)
;

where ARRAY['engineer', 'engineering'] @> roles

# Create temp table of hires from Thumbtack only
DROP TABLE IF EXISTS hires;
CREATE TEMP TABLE hires AS
SELECT id
      ,company_id
      ,hired
FROM   applicants
WHERE  company_id = 8
AND hired = TRUE
;

# Count estimate for applicants from Thumbtack
SELECT count_estimate('SELECT id
    FROM applicants
    WHERE company_id = 8')
;

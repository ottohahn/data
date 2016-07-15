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
    'Agencies',
    'Animal',
    'Awards',
    'Brands',
    'Character',
    'Communication',
    'Custom',
    'FieldTerminology',
    'JobTitle',
    'OperatingSystem',
    'Organization',
    'Organizations',
    'ProfessionalDegree',
    'Skill Cluster',
    'Software systems',
    'Technology')
;

-- # "kinds" to keep
-- Agencies
-- Animal
-- Awards
-- Brands
-- Character
-- Communication
-- Custom
-- FieldTerminology
-- JobTitle
-- OperatingSystem
-- Organization
-- Organizations
-- ProfessionalDegree
-- Skill Cluster
-- Software systems
-- Technology

-- # "kinds" to remove
-- Anatomy
-- Artifacts
-- Associations & groups
-- Automobile
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

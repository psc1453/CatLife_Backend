CREATE VIEW ExcreteErrorView AS
SELECT excrete_timestamp, type, excrete_status
FROM (SELECT urine_timestamp as excrete_timestamp, 'urine' AS 'type', urine_status AS excrete_status
      FROM UrineRecords
      UNION ALL
      SELECT stool_timestamp as excrete_timestamp, 'stool' AS 'type', stool_status AS excrete_status
      FROM StoolRecords) AS ExcreteRecords
WHERE excrete_status != 'normal';

CREATE VIEW ExcreteEverydayView AS
SELECT excrete_date, SUM(IF(type = 'urine', 1, 0)) AS 'urine', SUM(IF(type = 'stool', 1, 0)) AS 'stool'
FROM (SELECT DATE(urine_timestamp) as excrete_date, 'urine' AS 'type'
      FROM UrineRecords
      UNION ALL
      SELECT DATE(stool_timestamp) as excrete_date, 'stool' AS 'type'
      FROM StoolRecords) AS ExcreteRecords
GROUP BY excrete_date;


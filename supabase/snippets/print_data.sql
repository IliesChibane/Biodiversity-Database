SELECT
  payload->> 'CD_REF' AS INPN_ID,
  payload->>'Nom scientifique' AS nom_scientifique,
  payload->>'Nom anglais' AS nom_anglais,
  payload->>'Nom francais' AS nom_francais,
  payload->>'Classe' AS classe,
  payload->>'Ordre' AS ordre,
  payload->>'Famille' AS famille,
  payload->>'Genre' AS genre,
  payload->>'Genre' AS genre,
  payload->>'Groupe_1' AS Groupe_1,
  payload->>'Groupe_2' AS Groupe_2
FROM taxa;

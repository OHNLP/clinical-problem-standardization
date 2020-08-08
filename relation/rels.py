rels_int_to_text = {
    0: "anatomicalDirection",
    1: "bodySite",
    2: "clinicalStatus",
    3: "dueTo",
    4: "findingMethod",
    5: "interpretation",
    6: "negated",
    7: "otherwiseRelated",
    8: "risk",
    9: "stage",
    10: "associatedSignAndSymptom",
    11: "certainty",
    12: "course",
    13: "exacerbatingFactor",
    14: "historical",
    15: "laterality",
    16: "occurredFollowing",
    17: "periodicity",
    18: "severity",
    19: "verificationStatus",
    20: "extent"
}

rels_txt_to_int = {v: k for k, v in rels_int_to_text.items()}

rels_n = len(rels_int_to_text)
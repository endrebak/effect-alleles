import sys


import click
import json
import sys
import requests, argparse

import pandas as pd


def find_trait(rs_df, trait_aliases):

    trait_regex = "|".join(trait_aliases)
    trait_rows = rs_df.Trait.str.lower().str.contains(trait_regex)
    trait_df = rs_df[trait_rows].reset_index(drop=True)

    non_trait_df = rs_df[~trait_rows]

    if len(non_trait_df):
        wrong_traits = "\n".join(list(non_trait_df.Trait))
        snp = non_trait_df.RsID.iloc[0]
        search_trait = trait_aliases[0]
        print("When searching for the trait {}, we found the unrelated traits for SNP {}:\n{}".format(
            search_trait, snp, wrong_traits), file=sys.stderr)

    return trait_df


# def find_direction(trait_rows):

#     df = trait_rows

#     df = df.dropna()

#     increase = df.loc[df.Direction == "increase"].RiskAllele
#     decrease = df.loc[df.Direction == "decrease"].RiskAllele

    # if len(set(increase)) == 1 and len(set(decrease)) == 1:
    #     return increase.iloc[0], decrease.iloc[0]




def rsid_search(rs_ids):

    base_url = "http://www.ebi.ac.uk/gwas/beta/rest/api/"
    snps = "singleNucleotidePolymorphisms/"
    search = "search/findByRsId?rsId="

    snp_rows = []

    with click.progressbar(rs_ids, file=sys.stderr) as bar:

        for rs_id in bar:

            url = base_url + snps + search + rs_id

            snp_response = requests.get(url)

            snp_data = json.loads(snp_response.content)

            association_data = json.loads(requests.get(snp_data["_links"]["associations"]["href"]).content)

            associations = association_data["_embedded"]["associations"]

            for j, association in enumerate(associations):

                risk_allele_frequency = association["riskFrequency"]
                beta_number = association["betaNum"]
                beta_unit = association["betaUnit"]
                p_value = association["pvalue"]
                stdr = association["standardError"]

                study = json.loads(requests.get(association["_links"]["study"]["href"]).content)

                ancestries = study["ancestries"]

                nb_individuals_initial, nb_individuals_replication = 0, 0
                for ancestry in ancestries:
                    if ancestry["type"] == "initial":
                        nb_individuals_initial += ancestry["numberOfIndividuals"]
                    else:
                        nb_individuals_replication += ancestry["numberOfIndividuals"]


                pubmed_id = study["pubmedId"]

                title =  study["title"]
                publication = study["publication"]

                trait = study["diseaseTrait"]["trait"]

                direction = association["betaDirection"]

                for i, loci in enumerate(association["loci"]):

                    assert len(loci["strongestRiskAlleles"]) == 1, print(loci["strongestRiskAlleles"])

                    risk_allele = loci["strongestRiskAlleles"][0]["riskAlleleName"].split("-")[1]

                    rowdict = {"Title": title, "Trait": trait, "RiskAllele":
                               risk_allele, "Direction": direction,
                               "Publication": publication, "RsID": rs_id,
                               "PubmedID": pubmed_id, "RiskFrequency":
                               risk_allele_frequency, "BetaNumber":
                               beta_number, "BetaUnit": beta_unit, "PValue":
                               p_value, "StdError": stdr, "NInitial":
                               nb_individuals_initial, "NReplication":
                               nb_individuals_replication, "NTotal":
                               nb_individuals_replication + \
                               nb_individuals_initial}

                    snp_rows.append(rowdict)

        return snp_rows

import sys


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

def find_direction(trait_rows):

    df = trait_rows

    df = df.dropna()

    increase = df.loc[df.Direction == "increase"].RiskAllele
    decrease = df.loc[df.Direction == "decrease"].RiskAllele

    if len(set(increase)) == 1 and len(set(decrease)) == 1:
        return increase.iloc[0], decrease.iloc[0]

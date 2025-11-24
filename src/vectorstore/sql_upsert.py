from datetime import date
from src.vectorstore import SessionLocal, Cluster, Opinions


# upserting the Cluster and Opinion data to SQLdb
def sql_db_upsert(c_jn, o_jn):
    """
    Starting up DB session and then grabbing relevant metadata per record

    Args:
        c_jn: cluster json
        o_jn: opinion json
    """
    db = SessionLocal()

    # try getting an existing record, else create a new one
    try:
        cluster = db.get(Cluster, c_jn["id"])

        # no cluster = new cluster
        if not cluster:
            # Insert new cluster record if none
            cluster = Cluster(
                id=c_jn["id"],
                case_name=c_jn.get("case_name"),
                docket_number=c_jn.get("docket_number"),
                # need to pass in correct date format
                date_filed=date.fromisoformat(c_jn.get("date_filed")),
                citation=c_jn.get("citation"),
                absolute_url=c_jn.get("absolute_url"),
                precedential_status=c_jn.get("precedential_status"),
                raw_source=c_jn,  # raw json
            )
            db.add(cluster)
        # Else do an upsert of the record
        else:
            cluster.case_name = c_jn.get("case_name")
            cluster.docket_number = c_jn.get("docket_number")
            cluster.date_filed = date.fromisoformat(c_jn.get("date_filed"))
            cluster.citation = c_jn.get("citation")
            cluster.absolute_url = c_jn.get("absolute_url")
            cluster.precedential_status = c_jn.get("precedential_status")
            cluster.raw_source = c_jn  # raw json

        # db.add(cluster)

        # getting the opinion data
        opinions = db.get(Opinions, o_jn["id"])
        if not opinions:
            # insert new opinion record if nonexistent
            opinions = Opinions(
                id=o_jn["id"],
                cluster_id=c_jn["id"],
                author=o_jn.get("author"),
                raw_source=o_jn,
            )
            db.add(opinions)

        # Else do an upsert of the record
        else:
            # connecting to cluster
            opinions.cluster_id = c_jn["id"]
            opinions.author = o_jn.get("author")
            opinions.raw_source = o_jn

        # db.add(opinions)

        # saving changes
        db.commit()
    except Exception:
        db.rollback()
        raise
    # close even if fail
    finally:
        db.close()

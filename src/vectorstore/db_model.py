from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


# Clusters are the parent object
class Cluster(Base):
    """Database table for Cluster objects from CourtListener.

    Attributes:
        __tablename__ (str): SQL db table name.
        id: Unique identifier integer.
        case_name: String text for case name.
        docket_number: Related docket id number.
        date_filed: Date of the case filing.
        citation:
        absolute_url: Full URL to cluster on CourtListener.
        precedential_status: Any past precedents on the case
        raw_source: Full .json object of the cluster.
        created_at: Date the SQL Cluster object was created.
        updated_at: Date the SQL Cluster object was updated.
        opinions: Opinion objects related to the Cluster.
        chunks: Chunk objects related to the Cluster.
    """

    __tablename__ = "cluster"

    # unique id
    id = Column(BigInteger, primary_key=True)
    case_name = Column(Text)
    docket_number = Column(Text)
    date_filed = Column(Date)
    citation = Column(Text)
    absolute_url = Column(Text)
    precedential_status = Column(Text)
    raw_source = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relational part
    opinions = relationship("Opinions", back_populates="cluster")
    chunks = relationship("Chunk", back_populates="cluster")


# Opinions are the child object
class Opinions(Base):
    """Database table for Opinions objects from CourtListener.


    Attributes:
        __tablename__ (str): SQL db table name.
        id: Unique identifier integer.
        cluster_id: ID of related cluster for this Opinions object.
        author: Author of this Opinions object.
        raw_source: Full .json object of the cluster.
        created_at: Date the SQL Cluster object was created.
        updated_at: Date the SQL Cluster object was updated.
        cluster: Cluster Object related to the Opinions object.
        chunks: Chunk objects related to the Opinions.
    """

    __tablename__ = "opinions"

    # unique id
    id = Column(BigInteger, primary_key=True)
    cluster_id = Column(
        BigInteger, ForeignKey("cluster.id", ondelete="CASCADE"), nullable=False
    )
    author = Column(Text)
    raw_source = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relational part
    cluster = relationship("Cluster", back_populates="opinions")
    chunks = relationship("Chunk", back_populates="opinions")


# these are the embeddings for Chroma
class Chunk(Base):
    """Database table for Chunk objects from CourtListener.

    Attributes:
        __tablename__ (str): SQL db table name.
        id: Unique identifier integer.
        cluster_id: Id for related Cluster object.
        opinion_id: Id for related Opinions object.
        chroma_collection: Where Chunk is stored in chroma db.
        created_at: Date Chunk object was created
        cluster: Cluster Object related to the Chunk object.
        opinions: Opinions objects related to the Chunk.
    """

    __tablename__ = "chunks"

    id = Column(Text, primary_key=True)
    cluster_id = Column(
        BigInteger, ForeignKey("cluster.id", ondelete="CASCADE"), nullable=False
    )
    opinion_id = Column(
        BigInteger, ForeignKey("opinions.id", ondelete="CASCADE"), nullable=False
    )
    chunk_index = Column(Integer, nullable=False)
    chroma_collection = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relational part
    cluster = relationship("Cluster", back_populates="chunks")
    opinions = relationship("Opinions", back_populates="chunks")

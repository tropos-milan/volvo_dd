import rdflib
from snowflake_connection import SnowflakeConnector
import pandas as pd
import plotly.express as px

class SparqlRunner:
    def __init__(self, ttl_file='final.ttl'):
        self.ttl_file = ttl_file
        self.graph = rdflib.Graph()
        self.graph.parse(self.ttl_file, format="ttl")

    def run_sparql_query(self, resource_uri):
        sparql_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ddashboard: <https://dynamicdashboard.ilabt.imec.be/broker/ontologies/ddashboard#>

        SELECT ?database ?schema ?table ?column
        WHERE {
          <%s> rdf:type ?type ;
               ddashboard:hasDatabase ?database ;
               ddashboard:hasSchema ?schema ;
               ddashboard:hasTable ?table ;
               ddashboard:hasColumn ?column .
        }""" % resource_uri

        qres = self.graph.query(sparql_query)
        results = []
        for row in qres:
            results.append({
                'database': str(row.database),
                'schema': str(row.schema),
                'table': str(row.table),
                'column': str(row.column)
            })
        return results

    def get_first_result(self, resource_uri):
        results = self.run_sparql_query(resource_uri)
        return results[0] if results else None

    def build_sql_query(self, resource_uri):
        result = self.get_first_result(resource_uri)
        if result:
            return f"SELECT * FROM {result['database']}.{result['schema']}.{result['table']} limit 100000"
        else:
            return "No valid result to build SQL query."

    def get_col(self, resource_uri):
        result = self.get_first_result(resource_uri)
        return result['column']

    def change_uri(self, resource_uri):
        if "FluidConsumption" in resource_uri:
            # Replace 'FluidConsumption' with 'FluidHistoricalDataSource' and return
            return resource_uri.replace("FluidConsumption", "FluidHistoricalDataSource")
        else:
            # Append 'HistoricalDataSource' if no replacement is done
            return resource_uri + "HistoricalDataSource"
    
    def plot_results(self, resource_uri):
        full_uri = self.change_uri(resource_uri)

        y = self.get_col(full_uri)
        query = self.build_sql_query(full_uri)

        snow = SnowflakeConnector()
        df = snow.query_data(query)

        df2 = df[[y]].tail(1000)
        df1 = df[['timestamp']].tail(1000)
        df_combined = pd.concat([df1, df2], axis=1)

        # Plotting
        fig = px.scatter(df_combined, x=df_combined.columns[0], y=df_combined.columns[1], title='Scatter Plot of Two DataFrames')

        # Show plot
        fig.show()
        





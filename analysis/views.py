from rest_framework import viewsets
from .models import Product
from .serializers import AnalysisSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework import permissions
from django.db import connection
import pandas as pd
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)


def get_correlation_matrix(correlation: str):
    """
    This function calculates the correlation of the columns of Product model

    :param correlation: pearson / spearman
    :return: dict
    """
    # connect with the Product sqlite database
    with connection.cursor() as cursor:

        # execute the query to get all the rows from Product db
        cursor.execute("SELECT * FROM 'analysis_product'")

        # create a dictionary with column names as description and cells as it values
        columns = [col[0] for col in cursor.description]
        product_dict = [
            dict(zip(columns, row)) for row in cursor.fetchall()
        ]

        # convert dictionary into df
        product_df = pd.DataFrame(product_dict)

        # calculate correlation based on parameter passed
        if correlation.lower() == 'spearman':
            corr_df = product_df.corr(method="spearman")
        else:
            corr_df = product_df.corr()

        # convert df to dict and return
        return corr_df.to_dict()


class AnalysisView(viewsets.ViewSet):
    """
    Analysis view that calculates correlation for Product model in runtime.
    """
    # assign the serializer class and the permissions
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """
        This method responds to the GET request for analysis api and calculates
        correlation based on the parameter passed.
        :param request:
        :return:
        """
        correlation_method = request.query_params.get('correlation')

        if correlation_method is None:
            # display proper message if correlation query param is not passed
            return Response({'message': 'Pass correlation query parameter!'},
                            status=HTTP_400_BAD_REQUEST)

        elif correlation_method.lower() == 'spearman' or correlation_method.lower() == 'pearson':
            # return correlation json data
            data = get_correlation_matrix(correlation_method)
            return Response(data, status=HTTP_200_OK)

        else:
            # display error message if invalid correlation method is passed
            return Response({'error': correlation_method + ' correlation method is not supported!'},
                            status=HTTP_400_BAD_REQUEST)


class ProductView(viewsets.ModelViewSet):
    """
    Model view set to add, edit and remove products from the Product db
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    RunRealtimeReportRequest,
)
from google.oauth2 import service_account
from django.conf import settings
from datetime import datetime, timedelta
import os


class GoogleAnalyticsService:
    def __init__(self):
        credentials_path = settings.GA_CREDENTIALS_PATH
        self.property_id = settings.GA_PROPERTY_ID
        
        # if not os.path.exists(credentials_path):
        #     raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {credentials_path}")
        
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/analytics.readonly"]
        )
        
        self.client = BetaAnalyticsDataClient(credentials=credentials)
    
    def get_realtime_users(self):
        """Retorna número de usuários ativos em tempo real"""
        try:
            request = RunRealtimeReportRequest(
                property=f"properties/{self.property_id}",
                metrics=[Metric(name="activeUsers")],
            )
            response = self.client.run_realtime_report(request)
            
            if response.rows:
                return int(response.rows[0].metric_values[0].value)
            return 0
        except Exception as e:
            print(f"Erro ao buscar usuários em tempo real: {e}")
            return 0
    
    def get_overview_stats(self, days=30):
        """Retorna estatísticas gerais dos últimos X dias"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(
                    start_date=f"{days}daysAgo",
                    end_date="today"
                )],
                metrics=[
                    Metric(name="activeUsers"),
                    Metric(name="sessions"),
                    Metric(name="screenPageViews"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="bounceRate"),
                ],
            )
            
            response = self.client.run_report(request)
            
            if response.rows:
                row = response.rows[0]
                return {
                    'users': int(row.metric_values[0].value),
                    'sessions': int(row.metric_values[1].value),
                    'pageviews': int(row.metric_values[2].value),
                    'avg_session_duration': float(row.metric_values[3].value),
                    'bounce_rate': float(row.metric_values[4].value) * 100,
                }
            
            return {
                'users': 0,
                'sessions': 0,
                'pageviews': 0,
                'avg_session_duration': 0,
                'bounce_rate': 0,
            }
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return None
    
    def get_daily_visitors(self, days=30):
        """Retorna visitantes diários para gráfico"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(
                    start_date=f"{days}daysAgo",
                    end_date="today"
                )],
                dimensions=[Dimension(name="date")],
                metrics=[
                    Metric(name="activeUsers"),
                    Metric(name="sessions"),
                ],
                order_bys=[{"dimension": {"dimension_name": "date"}}]
            )
            
            response = self.client.run_report(request)
            
            data = []
            for row in response.rows:
                date_str = row.dimension_values[0].value
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                
                data.append({
                    'date': date_obj.strftime("%Y-%m-%d"),
                    'users': int(row.metric_values[0].value),
                    'sessions': int(row.metric_values[1].value),
                })
            
            return data
        except Exception as e:
            print(f"Erro ao buscar visitantes diários: {e}")
            return []
    
    def get_top_pages(self, limit=10):
        """Retorna as páginas mais visitadas"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(
                    start_date="30daysAgo",
                    end_date="today"
                )],
                dimensions=[
                    Dimension(name="pagePath"),
                    Dimension(name="pageTitle"),
                ],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="averageSessionDuration"),
                ],
                order_bys=[{"metric": {"metric_name": "screenPageViews"}, "desc": True}],
                limit=limit,
            )
            
            response = self.client.run_report(request)
            
            pages = []
            for row in response.rows:
                pages.append({
                    'path': row.dimension_values[0].value,
                    'title': row.dimension_values[1].value,
                    'views': int(row.metric_values[0].value),
                    'avg_time': float(row.metric_values[1].value),
                })
            
            return pages
        except Exception as e:
            print(f"Erro ao buscar páginas mais visitadas: {e}")
            return []
    
    def get_traffic_sources(self):
        """Retorna fontes de tráfego"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(
                    start_date="30daysAgo",
                    end_date="today"
                )],
                dimensions=[Dimension(name="sessionSource")],
                metrics=[
                    Metric(name="sessions"),
                    Metric(name="activeUsers"),
                ],
                order_bys=[{"metric": {"metric_name": "sessions"}, "desc": True}],
                limit=10,
            )
            
            response = self.client.run_report(request)
            
            sources = []
            for row in response.rows:
                sources.append({
                    'source': row.dimension_values[0].value,
                    'sessions': int(row.metric_values[0].value),
                    'users': int(row.metric_values[1].value),
                })
            
            return sources
        except Exception as e:
            print(f"Erro ao buscar fontes de tráfego: {e}")
            return []
    
    def get_top_cavalos(self, limit=20):
        """Retorna os cavalos mais visualizados"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(
                    start_date="30daysAgo",
                    end_date="today"
                )],
                dimensions=[
                    Dimension(name="pagePath"),
                    Dimension(name="pageTitle"),
                ],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="sessionsPerUser"),
                ],
                dimension_filter={
                    "filter": {
                        "field_name": "pagePath",
                        "string_filter": {
                            "match_type": "CONTAINS",
                            "value": "/cavalo/"
                        }
                    }
                },
                order_bys=[{"metric": {"metric_name": "screenPageViews"}, "desc": True}],
                limit=limit,
            )
            
            response = self.client.run_report(request)
            
            cavalos = []
            for row in response.rows:
                path = row.dimension_values[0].value
                cavalo_id = path.split('/')[-2] if '/' in path else None
                
                cavalos.append({
                    'path': path,
                    'title': row.dimension_values[1].value,
                    'cavalo_id': cavalo_id,
                    'views': int(row.metric_values[0].value),
                    'avg_time': float(row.metric_values[1].value),
                    'engagement': float(row.metric_values[2].value),
                })
            
            return cavalos
        except Exception as e:
            print(f"Erro ao buscar cavalos mais acessados: {e}")
            return []
    
    def get_cavalo_stats(self, cavalo_slug_or_id):
        """Retorna estatísticas de um cavalo específico"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(
                    start_date="90daysAgo",
                    end_date="today"
                )],
                dimensions=[Dimension(name="date")],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers"),
                    Metric(name="averageSessionDuration"),
                ],
                dimension_filter={
                    "filter": {
                        "field_name": "pagePath",
                        "string_filter": {
                            "match_type": "CONTAINS",
                            "value": f"/cavalo/{cavalo_slug_or_id}"
                        }
                    }
                },
                order_bys=[{"dimension": {"dimension_name": "date"}}]
            )
            
            response = self.client.run_report(request)
            
            daily_stats = []
            for row in response.rows:
                date_str = row.dimension_values[0].value
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                
                daily_stats.append({
                    'date': date_obj.strftime("%Y-%m-%d"),
                    'views': int(row.metric_values[0].value),
                    'users': int(row.metric_values[1].value),
                    'avg_time': float(row.metric_values[2].value),
                })
            
            return daily_stats
        except Exception as e:
            print(f"Erro ao buscar estatísticas do cavalo: {e}")
            return []
    
    def get_cavalos_comparison(self, days=30):
        """Compara performance de todos os cavalos"""
        try:
            # Retorna dados do Google Analytics
            return self.get_top_cavalos(limit=50)
        except Exception as e:
            print(f"Erro ao comparar cavalos: {e}")
            return []
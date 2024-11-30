# -*- coding: utf-8 -*-
"""23살인생최후의파이썬끌어치기.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hOENjrktSj5J85tAhgUQ_QCFiZNr8X4R
"""

!apt-get install -y fonts-nanum
!fc-cache -fv
!rm ~/.cache/matplotlib -rf

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 폰트 설정
plt.rc('font', family='NanumBarunGothic')

class AdPerformanceAnalyzer:
    def __init__(self, file_path):
        """광고 성과 분석기 초기화
        Args:
            file_path (str): CSV 파일 경로
        """
        self.file_path = file_path
        self.data = None  # 원본 데이터
        self.cleaned_data = None  # 자른 데이터

    def load_and_clean_data(self):

        # 데이터 로드
        df = pd.read_csv(self.file_path)

        # 사용하지 않는 열 제거 (정제)
        columns_to_drop = [
            '광고 세트 게재', '기여 설정', '광고 세트 예산', '광고 세트 예산 유형',
            '종료', '시작', '결과 표시 도구', '결과'
        ]
        df_cleaned = df.drop(columns=columns_to_drop)

        # 컬럼명 수정
        column_rename = {
            'CPM(1000회 노출당 비용) (KRW)': 'CPM',
            'CPC(링크 클릭당 비용) (KRW)': 'CPC_링크',
            'CTR(링크 클릭률)': 'CTR_링크',
            'CPC(전체) (KRW)': 'CPC_전체',
            'CTR(전체)': 'CTR_전체',
            '계정 센터 계정 1000개 도달당 비용 (KRW)': '도달당_비용',
            '지출 금액 (KRW)': '지출 금액'
        }
        df_cleaned = df_cleaned.rename(columns=column_rename)

        # '광고 세트 이름'을 캠페인 유형과 세부 유형으로 분리
        df_cleaned[['캠페인_유형', '세부_유형']] = df_cleaned['광고 세트 이름'].str.split('_', expand=True)

        # 정제된 데이터를 저장
        self.cleaned_data = df_cleaned
        return df_cleaned

    def create_cost_efficiency_plot(self):

        plt.figure(figsize=(12, 8))

        # CPC와 CTR 간의 관계를 캠페인 유형별로 시각화
        sns.scatterplot(
            data=self.cleaned_data,
            x='CPC_링크',
            y='CTR_링크',
            hue='캠페인_유형',
            size='지출 금액',
            sizes=(100, 500),
            alpha=0.6
        )

        # 그래프 제목과 축 레이블 설정
        plt.title('광고 캠페인 비용 효율성 분석\n(CPC vs CTR)', pad=20)
        plt.xlabel('링크 클릭당 비용 (CPC, 원)')
        plt.ylabel('링크 클릭률 (CTR, %)')

        # 범례 위치 조정
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()  # 그래프 요소 간 간격 조정

        return plt.gcf()  # 현재 그래프 객체 반환 (main init에서 그린다.)

    def create_reach_analysis_plot(self):
        """도달 효과 분석 시각화"""
        plt.figure(figsize=(12, 8))

        # 지출 금액과 도달 수 간의 관계를 시각화
        sns.regplot(
            data=self.cleaned_data,
            x='지출 금액',
            y='도달',
            scatter_kws={'alpha': 0.5},
            line_kws={'color': 'red'}
        )

        # 그래프 제목과 라벨 설정
        plt.title('광고 지출 금액 대비 도달 효과 분석', pad=20)
        plt.xlabel('지출 금액 (원)')
        plt.ylabel('도달 수')

        plt.tight_layout()
        return plt.gcf()

    def create_campaign_comparison_plot(self):

        # 캠페인 유형별 주요 지표(CPC, CTR, CPM)의 평균 계산
        campaign_stats = self.cleaned_data.groupby('캠페인_유형').agg({
            'CPC_링크': 'mean',  # CPC 평균
            'CTR_링크': 'mean',  # CTR 평균
            'CPM': 'mean'  # CPM 평균
        }).reset_index()

        # 그래프 생성
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

        # 캠페인별 CPC 비교
        sns.barplot(data=campaign_stats, x='캠페인_유형', y='CPC_링크', ax=ax1, color='skyblue')
        ax1.set_title('캠페인 유형별 평균 CPC')
        ax1.tick_params(axis='x', rotation=45)

        # 캠페인별 CTR 비교
        sns.barplot(data=campaign_stats, x='캠페인_유형', y='CTR_링크', ax=ax2, color='lightgreen')
        ax2.set_title('캠페인 유형별 평균 CTR')
        ax2.tick_params(axis='x', rotation=45)

        # 캠페인별 CPM 비교
        sns.barplot(data=campaign_stats, x='캠페인_유형', y='CPM', ax=ax3, color='salmon')
        ax3.set_title('캠페인 유형별 평균 CPM')
        ax3.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return plt.gcf()

    def generate_insights(self):

      # 데이터 기반 인사이트 생성
      insights = []

      # 1. 기존의 기본 인사이트 생성
      # CTR 기준 상위 3개 캠페인
      best_ctr = self.cleaned_data.nlargest(3, 'CTR_링크')[['광고 세트 이름', 'CTR_링크']]
      insights.append("\n=== CTR 기준 상위 캠페인 ===")
      for _, row in best_ctr.iterrows():
          insights.append(f"- {row['광고 세트 이름']}: CTR {row['CTR_링크']:.2f}%")

      # 2. 캠페인 유형별 성과 분석
      campaign_types = self.cleaned_data.groupby('캠페인_유형').agg({
          'CTR_링크': 'mean',
          'CPC_링크': 'mean'
      }).round(2)

      best_campaign = campaign_types['CTR_링크'].idxmax()
      insights.append(f"\n=== 캠페인 유형별 분석 ===")
      insights.append(f"- 가장 효과적인 캠페인 유형: {best_campaign}")
      insights.append(f"  - 평균 CTR: {campaign_types.loc[best_campaign, 'CTR_링크']}%")
      insights.append(f"  - 평균 CPC: {campaign_types.loc[best_campaign, 'CPC_링크']}원")

      # 3. 개선 제안사항 생성
      insights.append("\n=== 개선 제안사항 ===")

      # 3-1. 비용 효율성 개선이 필요한 캠페인 식별
      avg_cpc = self.cleaned_data['CPC_링크'].mean()
      high_cost_campaigns = self.cleaned_data[
          self.cleaned_data['CPC_링크'] > avg_cpc * 1.2
      ]['광고 세트 이름'].tolist()

      if high_cost_campaigns:
          insights.append("비용 효율성 개선 필요 캠페인:")
          for campaign in high_cost_campaigns:
              insights.append(f"- {campaign}: CPC가 평균보다 20% 이상 높습니다")

      # 3-2. 성과 개선이 필요한 캠페인들 식별
      # 평균값 계산
      avg_ctr = self.cleaned_data['CTR_링크'].mean()
      avg_cpm = self.cleaned_data['CPM'].mean()
      avg_cpc = self.cleaned_data['CPC_링크'].mean()

      # CTR이 낮은 캠페인 식별 (평균보다 10% 이상 낮은 경우)
      low_performing_campaigns = self.cleaned_data[
          self.cleaned_data['CTR_링크'] < avg_ctr * 0.9  # 0.8에서 0.9로 변경
      ]['광고 세트 이름'].tolist()

      # CPM이 높은 캠페인 식별 (평균보다 10% 이상 높은 경우)
      high_cpm_campaigns = self.cleaned_data[
          self.cleaned_data['CPM'] > avg_cpm * 1.1  # 1.2에서 1.1로 변경
      ]['광고 세트 이름'].tolist()

      # CPC가 높은 캠페인 식별 (평균보다 5% 이상 높은 경우)
      high_cpc_campaigns = self.cleaned_data[
          self.cleaned_data['CPC_링크'] > avg_cpc * 1.05  # 1.2에서 1.05로 변경
      ]['광고 세트 이름'].tolist()

      insights.append("\n=== 성과 개선 필요 캠페인 분석 ===")

      # CTR 관련 인사이트
      if low_performing_campaigns:
          insights.append("\n■ 클릭률(CTR) 개선 필요 캠페인:")
          insights.append(f"  - 전체 평균 CTR: {avg_ctr:.2f}%")
          for campaign in low_performing_campaigns:
              campaign_ctr = self.cleaned_data[
                  self.cleaned_data['광고 세트 이름'] == campaign
              ]['CTR_링크'].iloc[0]
              insights.append(f"  - {campaign}")
              insights.append(f"    • 현재 CTR: {campaign_ctr:.2f}%")
              insights.append(f"    • 평균 대비: {((campaign_ctr - avg_ctr)/avg_ctr * 100):.1f}% 낮음")
              insights.append(f"    • 제안: 광고 크리에이티브 개선 및 타겟팅 재검토 필요")

      # CPM 관련 인사이트
      if high_cpm_campaigns:
          insights.append("\n■ 노출비용(CPM) 개선 필요 캠페인:")
          insights.append(f"  - 전체 평균 CPM: {avg_cpm:.0f}원")
          for campaign in high_cpm_campaigns:
              campaign_cpm = self.cleaned_data[
                  self.cleaned_data['광고 세트 이름'] == campaign
              ]['CPM'].iloc[0]
              insights.append(f"  - {campaign}")
              insights.append(f"    • 현재 CPM: {campaign_cpm:.0f}원")
              insights.append(f"    • 평균 대비: {((campaign_cpm - avg_cpm)/avg_cpm * 100):.1f}% 높음")
              insights.append(f"    • 제안: 입찰가 조정 및 타겟 오디언스 범위 확대 검토")

      # CPC 관련 인사이트
      if high_cpc_campaigns:
          insights.append("\n■ 클릭비용(CPC) 개선 필요 캠페인:")
          insights.append(f"  - 전체 평균 CPC: {avg_cpc:.0f}원")
          for campaign in high_cpc_campaigns:
              campaign_cpc = self.cleaned_data[
                  self.cleaned_data['광고 세트 이름'] == campaign
              ]['CPC_링크'].iloc[0]
              insights.append(f"  - {campaign}")
              insights.append(f"    • 현재 CPC: {campaign_cpc:.0f}원")
              insights.append(f"    • 평균 대비: {((campaign_cpc - avg_cpc)/avg_cpc * 100):.1f}% 높음")
              insights.append(f"    • 제안: 키워드 최적화 및 광고 품질점수 개선 필요")

      # 종합 개선 제안
      if any([low_performing_campaigns, high_cpm_campaigns, high_cpc_campaigns]):
          insights.append("\n■ 종합 개선 제안:")
          if len(set(low_performing_campaigns) & set(high_cpc_campaigns)) > 0:
              insights.append("  - CTR과 CPC 모두 개선이 필요한 캠페인이 있습니다. 이 캠페인들은 우선적으로 개선이 필요합니다.")
          if high_cpm_campaigns:
              insights.append("  - CPM이 높은 캠페인들은 타겟팅을 넓히거나 입찰 전략을 수정해보세요.")
          insights.append("  - 성과가 좋은 캠페인의 타겟팅과 크리에이티브 전략을 참고하여 적용해보세요.")


      # 새로운 섹션: 콘텐츠 및 타겟팅 분석
      insights.append("\n=== 콘텐츠 및 타겟팅 최적화 분석 ===")

      # 콘텐츠 효과 분석
      content_data = self.cleaned_data[
          self.cleaned_data['세부_유형'].isin(['이미지', '영상'])  # '비디오' 제거
      ]

      if not content_data.empty:
          content_patterns = content_data.groupby('세부_유형').agg({
              'CTR_링크': 'mean',
              'CPC_링크': 'mean',
              'CPM': 'mean',
              '도달': 'mean'
          }).round(2)

          best_content = content_patterns['CTR_링크'].idxmax()
          insights.append("\n■ 콘텐츠 최적화 제안:")
          insights.append(f"  - {best_content} 형식의 광고가 가장 효과적:")
          insights.append(f"    • 평균 CTR: {content_patterns.loc[best_content, 'CTR_링크']:.2f}%")
          insights.append(f"    • 평균 CPC: {content_patterns.loc[best_content, 'CPC_링크']:.0f}원")
          insights.append(f"    • 평균 도달: {content_patterns.loc[best_content, '도달']:.0f}명")
          insights.append(f"  - 제안: {best_content} 형식의 콘텐츠 비중을 늘리고, 다른 캠페인의 크리에이티브도 이 형식을 참고하세요.")

      # 타겟팅 효과 분석
      targeting_data = self.cleaned_data[
          (self.cleaned_data['캠페인_유형'].isin(['신규', '재방문'])) |
          (self.cleaned_data['세부_유형'].isin(['20대', '30대', '기업', '개인']))
      ]

      if not targeting_data.empty:
          targeting_patterns = targeting_data.groupby('광고 세트 이름').agg({
              'CTR_링크': 'mean',
              'CPC_링크': 'mean',
              'CPM': 'mean',
              '도달': 'mean'
          }).round(2)

          efficient_target = targeting_patterns['CPC_링크'].idxmin()
          best_performing_target = targeting_patterns['CTR_링크'].idxmax()

          insights.append("\n■ 타겟팅 최적화 제안:")
          insights.append(f"  - 비용 효율이 가장 좋은 타겟팅: {efficient_target}")
          insights.append(f"    • CPC: {targeting_patterns.loc[efficient_target, 'CPC_링크']:.0f}원")
          insights.append(f"    • CTR: {targeting_patterns.loc[efficient_target, 'CTR_링크']:.2f}%")

          if efficient_target != best_performing_target:
              insights.append(f"  - CTR이 가장 높은 타겟팅: {best_performing_target}")
              insights.append(f"    • CTR: {targeting_patterns.loc[best_performing_target, 'CTR_링크']:.2f}%")

          insights.append("  - 제안:")
          insights.append(f"    • 비용 효율이 좋은 {efficient_target} 타겟팅의 예산 비중을 늘리세요.")
          insights.append(f"    • 유사 잠재고객을 활용하여 타겟 그룹을 확장해보세요.")


      return "\n".join(insights)

if __name__ == "__main__":
    # 분석기 초기화 및 데이터 로드
    analyzer = AdPerformanceAnalyzer("/content/meta-ad-data.csv")
    analyzer.load_and_clean_data()

    # 시각화 생성
    cost_plot = analyzer.create_cost_efficiency_plot()
    reach_plot = analyzer.create_reach_analysis_plot()
    campaign_plot = analyzer.create_campaign_comparison_plot()

    # 인사이트 생성 및 출력
    insights = analyzer.generate_insights()
    print(insights)

    # 그래프 표시
    plt.show()

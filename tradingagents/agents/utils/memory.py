import chromadb
from chromadb.config import Settings
from openai import OpenAI


class FinancialSituationMemory:
    def __init__(self, name=None, config=None):
        # 本地模式，只做最简单的文本存储检索
        self.situations = []
        self.advice = []

    def add_situations(self, situations_and_advice):
        for situation, recommendation in situations_and_advice:
            self.situations.append(situation)
            self.advice.append(recommendation)

    def get_memories(self, current_situation, n_matches=1):
        # 简单字符串相似度检索，选最长公共子串最多的N条
        def simple_similarity(a, b):
            return sum(1 for w in a.split() if w in b.split())

        scores = [simple_similarity(current_situation, s) for s in self.situations]
        ranked = sorted(zip(scores, self.situations, self.advice), reverse=True)
        results = []
        for i, (score, s, rec) in enumerate(ranked[:n_matches]):
            results.append({
                "matched_situation": s,
                "recommendation": rec,
                "similarity_score": score,
            })
        return results


if __name__ == "__main__":
    # Example usage
    matcher = FinancialSituationMemory()

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors 
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")

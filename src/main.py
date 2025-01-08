from extract import extract_pdf_single, extract_pdf_folder
from conference_selection import cvpr_suggestion, neurips_suggestion, emnlp_suggestion, kdd_suggestion, tmlr_suggestion, final_conference
from evaluator import evaluate


if __name__ == "__main__":
    research_paper = extract_pdf_single('/Users/nisarg/Desktop/KGP_DS/R008.pdf')
    benchmark_list = extract_pdf_folder('/Users/nisarg/Desktop/Kgp_pathway/src')
    benchmark_papers = ""
    for benchmark_paper in benchmark_list:
        benchmark_papers += benchmark_paper + '\n'
    evaluation_result = evaluate(research_paper, benchmark_papers)
    print(evaluation_result)    
    if(evaluation_result == "Yes"):
        # print(cvpr_suggestion(research_paper))
        # print(neurips_suggestion(research_paper))
        # print(emnlp_suggestion(research_paper))
        # print(kdd_suggestion(research_paper))
        # print(tmlr_suggestion(research_paper))
        print(final_conference(research_paper))
    else:
        print("Not suitable for publication")


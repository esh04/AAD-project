from PyScripts.divide_and_conquer import guess_socks, rand_num
from PyScripts.n_queens import check_n_queens

from flask import Flask, render_template, request, session
from flask_session import Session
from math import log, ceil

app = Flask(__name__)

# Configure session to use as filesystem
app.secret_key = 'superSecretKey'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/divide-and-conquer", methods=["GET","POST"])
def divide_and_conquer():
  if request.method == "GET":
    session["total_socks"] = rand_num(10,50)
    session["max_tries"] = ceil(log(session["total_socks"],2))
    session["num"] = rand_num(1,10)
    session["text"] = "Guess among the socks numbered  1 to {}. Number of tries you have are {}".format(session["total_socks"], session["max_tries"])
    session["wrong_answers"] = 0
    session["hint"] = ''
    return render_template("divide-and-conquer.html")
  elif request.method == "POST":
    if request.form.get("sock"):
      session["guess"] = int(request.form.get("sock"))
      session["text"], session["wrong_answers"] = guess_socks(session["num"], session["guess"], session["wrong_answers"],session["max_tries"])
    elif request.form.get("hint"):
          session["hint"] = "A win in the given amount of tries is guaranteed if one uses the divide and conquer algorithm. Divide the set into two, after recieving the prompt you can then eliminate one of the sets. Keep doing so on the newly required set until you are left with only one sock."
    else:
          session["text"] = "Please choose a sock."
    return render_template("divide-and-conquer.html")
      


@app.route("/n-queens", methods=["GET","POST"])
def n_queens():
  if request.method == "GET":
    hint=''
    # session["N"] = 4
    session["N"] = rand_num(6,10)

    return render_template("n-queens.html",  text='',hint=hint, N = session["N"])
  elif request.method == "POST":
    if request.form.get("check-square"):
      checked = (request.form.getlist("check-square"))
      if len(checked) == session["N"]:
          if check_n_queens(checked, session["N"]) == 1: 
            text = "Congratulations! You have solved the problem. You can look for more solutions if you wish."
          else:
            text = "Sorry, your solution was wrong. Please try again"
      else:
            text = "Please choose EXACTLY {} squares.".format(session["N"])
      return render_template("n-queens.html", text=text,hint='', N = session["N"])
            
    elif request.form.get("hint"):
          hint = "You can use backstrapping to solve the problem."
          return render_template("n-queens.html", text='',hint=hint, N = session["N"])

    else:
          text = "Please choose the positions where you wish to place the queens."
          return render_template("n-queens.html", text=text,hint='', N = session["N"])


@app.route("/partition", methods=["GET","POST"])
def partition():
  if request.method == "GET":
    session["numbers"]=[10,12,4,9,19,17,1,25,3,2,7,8]
    hint=''
    return render_template("partition.html",  text='',hint=hint)
  elif request.method == "POST":
    if request.form.get('partition1') and request.form.get('partition2') and request.form.get('partition3'):
      partition1 = request.form.get('partition1').split(',')
      partition2 = request.form.get('partition2').split(',')
      partition3 = request.form.get('partition3').split(',')
      partition1 = set(map(int, partition1))
      partition2 = set(map(int, partition2))
      partition3 = set(map(int, partition3))
      print(partition1, partition2, partition3)
      allnums = set(session["numbers"])
      if partition1.issubset(allnums) and partition2.issubset(allnums) and partition3.issubset(allnums):
            if sum(partition1) == sum(partition2) == sum(partition3):
                  text = "You are correct!"
            else:
                  print(sum(partition1), sum(partition2), sum(partition3))
                  text = "Sorry, your solution was wrong. Please try again"
      else:
            text = "Please give valid input. You have either not chosen numbers from the list or have not comma seprated them."

      return render_template("partition.html", text=text,hint='')
            
    elif request.form.get("hint"):
          hint = "Following are the two main steps to solve this problem:"
          return render_template("partition.html", text='',hint=hint)

    else:
          text = "Please partition the numbers."
          return render_template("partition.html", text=text,hint='')

@app.route("/info-backtracking", methods=["GET"])
def backtracking():
    heading='Backtracking'
    text1="Backtracking is an algorithmic-technique for solving problems recursively by trying to build a solution incrementally, one piece at a time, removing those solutions that fail to satisfy the constraints of the problem at any point of time (by time, here, is referred to the time elapsed till reaching any level of the search tree)."
    text2="For example, consider the SudoKo solving Problem, we try filling digits one by one. Whenever we find that current digit cannot lead to a solution, we remove it (backtrack) and try next digit. This is better than naive approach (generating all possible combinations of digits and then trying every combination one by one) as it drops a set of permutations whenever it backtracks."
    text3="We’re taking a very simple example here in order to explain the theory behind a backtracking process. We want to arrange the three letters a, b, c in such a way that c cannot be beside a."

    text4 = "According to the backtracking, first, we’ll build a state-space tree. We’ll find all the possible solutions and check them with the given constraint. We’ll only keep those solutions that satisfy the given constraint:"
    text5="The backtracking algorithm is applied to some specific types of problems. For instance, we can use it to find a feasible solution to a decision problem. It was also found to be very effective for optimization problems."
    text6="For some cases, a backtracking algorithm is used for the enumeration problem in order to find the set of all feasible solutions for the problem."
    img = 'https://www.baeldung.com/wp-content/uploads/sites/4/2020/11/1-4-2.png'
    link="https://www.geeksforgeeks.org/backtracking-algorithms/"
    return render_template("info.html", heading=heading, text1=text1, text2=text2,text3=text3,text4=text4,text5=text5,text6=text6,image=img,link=link)

@app.route("/info-greedy", methods=["GET"])
def greedy():
    heading='Greedy Algorithm'
    text1="A greedy algorithm is a simple, intuitive algorithm that is used in optimization problems. The algorithm makes the optimal choice at each step as it attempts to find the overall optimal way to solve the entire problem. Greedy algorithms are quite successful in some problems, such as Huffman encoding which is used to compress data, or Dijkstra's algorithm, which is used to find the shortest path through a graph. "
    text2="However, in many problems, a greedy strategy does not produce an optimal solution. For example, in the animation below, the greedy algorithm seeks to find the path with the largest sum. It does this by selecting the largest available number at each step. The greedy algorithm fails to find the largest sum, however, because it makes decisions based only on the information it has at any one step, without regard to the overall problem. "
    text4="Greedy algorithm will work only if the following two conditions are satisfied:"
    text5="Greedy choice property: A global (overall) optimal solution can be reached by choosing the optimal choice at each step."
    text6="Optimal substructure: A problem has an optimal substructure if an optimal solution to the entire problem contains the optimal solutions to the sub-problems."

    img = 'https://www.codingninjas.com/blog/wp-content/uploads/2020/06/CC3.png'
    link="https://www.geeksforgeeks.org/greedy-algorithms/"
    return render_template("info.html", heading=heading, text1=text1, text2=text2,text4=text4,text5=text5,text6=text6,image=img,link=link)

@app.route("/info-dynamic", methods=["GET"])
def dynamic():
    heading='Dynamic Algorithm'
    text1 = "Dynamic programming approach is similar to divide and conquer in breaking down the problem into smaller and yet smaller possible sub-problems. But unlike, divide and conquer, these sub-problems are not solved independently. Rather, results of these smaller sub-problems are remembered and used for similar or overlapping sub-problems."
    text2 = "Dynamic programming is used where we have problems, which can be divided into similar sub-problems, so that their results can be re-used. Mostly, these algorithms are used for optimization. Before solving the in-hand sub-problem, dynamic algorithm will try to examine the results of the previously solved sub-problems. The solutions of sub-problems are combined in order to achieve the best solution."
    text4="Finding the shortest path in a graph using optimal substructure; a straight line indicates a single edge; a wavy line indicates a shortest path between the two vertices it connects (among other paths, not shown, sharing the same two vertices); the bold line is the overall shortest path from start to goal."
    text5="In contrast to greedy algorithms, where local optimization is addressed, dynamic algorithms are motivated for an overall optimization of the problem."
    text6="In contrast to divide and conquer algorithms, where solutions are combined to achieve an overall solution, dynamic algorithms use the output of a smaller sub-problem and then try to optimize a bigger sub-problem. Dynamic algorithms use Memoization to remember the output of already solved sub-problems."
    img="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Shortest_path_optimal_substructure.svg/1200px-Shortest_path_optimal_substructure.svg.png"
    link='https://www.geeksforgeeks.org/dynamic-programming/'
    return render_template("info.html", heading=heading, text1=text1, text2=text2,text4=text4, text5=text5, text6=text6 ,image=img,link=link)

@app.route("/info-divide-and-conquer", methods=["GET"])
def divide():
    heading='Divide and Conquer'
    text1="In divide and conquer approach, the problem in hand, is divided into smaller sub-problems and then each problem is solved independently. When we keep on dividing the subproblems into even smaller sub-problems, we may eventually reach a stage where no more division is possible. Those 'atomic' smallest possible sub-problem (fractions) are solved. The solution of all sub-problems is finally merged in order to obtain the solution of an original problem."
    text3="Broadly, we can understand divide-and-conquer approach in a three-step process."
    text4="Divide/Break: This step involves breaking the problem into smaller sub-problems. Sub-problems should represent a part of the original problem. This step generally takes a recursive approach to divide the problem until no sub-problem is further divisible. At this stage, sub-problems become atomic in nature but still represent some part of the actual problem."
    text5="Conquer/Solve: This step receives a lot of smaller sub-problems to be solved. Generally, at this level, the problems are considered 'solved' on their own."
    text6="Merge/Combine: When the smaller sub-problems are solved, this stage recursively combines them until they formulate a solution of the original problem. This algorithmic approach works recursively and conquer & merge steps works so close that they appear as one."

    img="https://www.tutorialspoint.com/data_structures_algorithms/images/divide_and_conquer.jpg"
    link='https://www.geeksforgeeks.org/divide-and-conquer-algorithm-introduction/'
    return render_template("info.html", heading=heading, text1=text1, text3=text3,text4=text4, text5=text5, text6=text6,image=img,link=link)

@app.route("/info-branch and bound", methods=["GET"])
def branch():
    heading='Branch and Bound'
    text1="Branch and bound is one of the techniques used for problem solving. It is similar to the backtracking since it also uses the state space tree. It is used for solving the optimization problems and minimization problems. If we have given a maximization problem then we can convert it using the Branch and bound technique by simply converting the problem into a maximization problem."
    text2="Let’s see the Branch and Bound Approach to solve the 0/1 Knapsack problem: The Backtracking Solution can be optimized if we know a bound on best possible solution subtree rooted with every node. If the best in subtree is worse than current best, we can simply ignore this node and its subtrees. So we compute bound (best solution) for every node and compare the bound with current best solution before exploring the node."
    text3="Example bounds used in below diagram are, A down can give $315, B down can $275, C down can $225, D down can $125 and E down can $30."
    img="https://media.geeksforgeeks.org/wp-content/uploads/knapsack3.jpg"
    link='https://www.javatpoint.com/branch-and-bound'
    return render_template("info.html", heading=heading, text1=text1, text2=text2,text3=text3,image=img,link=link)

@app.route("/info-searching-algorithms", methods=["GET"])
def searching():
    heading='Searching Algorithms'
    text1="Searching Algorithms are designed to check for an element or retrieve an element from any data structure where it is stored. Based on the type of search operation, these algorithms are generally classified into two categories:"
    text2="Sequential Search: In this, the list or array is traversed sequentially and every element is checked. For example: Linear Search."
    text3="Interval Search: These algorithms are specifically designed for searching in sorted data-structures. These type of searching algorithms are much more efficient than Linear Search as they repeatedly target the center of the search structure and divide the search space in half. For Example: Binary Search."
    text4="Some of the other commonly used searching algorithms are: Jump search, Interpolation Search, Exponential Search, Fibonacci Search, etc." 
    img="https://i.ytimg.com/vi/sSYQ1H9-Vks/maxresdefault.jpg"
    link='https://www.geeksforgeeks.org/searching-algorithms/'
    return render_template("info.html", heading=heading, text1=text1, text2=text2,text3=text3,image=img,link=link,text4=text4)

@app.route("/info-sorting-algorithms", methods=["GET"])
def sorting():
    heading='Sorting Algorithms'
    text1 = "A Sorting Algorithm is used to rearrange a given array or list elements according to a comparison operator on the elements. The comparison operator is used to decide the new order of element in the respective data structure."
    text2="The importance of sorting lies in the fact that data searching can be optimized to a very high level, if data is stored in a sorted manner. Sorting is also used to represent data in more readable formats."
    text3="For example: The below list of characters is sorted in increasing order of their ASCII values. That is, the character with lesser ASCII value will be placed first than the character with higher ASCII value."
    text4="Some of the very commonly used sorting algorithms are: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, Heap Sort, Bucket sort, Shell sort etc."
    img="https://www.geeksforgeeks.org/wp-content/uploads/sorting-algorithms.jpg"
    link='https://www.tutorialspoint.com/data_structures_algorithms/sorting_algorithms.htm'
    return render_template("info.html", heading=heading, text1=text1, text2=text2,text3=text3,image=img,link=link,text4=text4)

@app.route("/info-randomized-algorithms", methods=["GET"])
def random():
    heading='Randomized Algorithms'
    text1 = "A randomized algorithm is a technique that uses a source of randomness as part of its logic. It is typically used to reduce either the running time, or time complexity; or the memory used, or space complexity, in a standard algorithm. The algorithm works by generating a random number, rrr, within a specified range of numbers, and making decisions based on rrr's value"
    text2="A randomized algorithm could help in a situation of doubt by flipping a coin or a drawing a card from a deck in order to make a decision. Similarly, this kind of algorithm could help speed up a brute force process by randomly sampling the input in order to obtain a solution that may not be totally optimal, but will be good enough for the specified purposes."
    text3="For example, A superintendent is attempting to score a high school based on several metrics, and she wants to do so from information gathered by confidentially interviewing students. However, the superintendent has to do this with all the schools in the district, so interviewing every single student would take a time she cannot afford. What should she do?"
    text4="The superintendent should employ a randomized algorithm, where, without knowing any of the kids, she’d select a few at random and interview them, hoping that she gets a wide variety of students. This technique is more commonly known as random sampling, which is a kind of randomized algorithm. Of course, she knows that there are diminishing returns from each additional interview, and should stop when the quantity of data collected measures what she was trying to measure to an acceptable degree of accuracy. The way that the superintendent is determining the score of the school can be thought of as a randomized algorithm. "   
    img="https://iq.opengenus.org/content/images/2020/09/Randomized-Flowchart-1.png"
    link='https://www.geeksforgeeks.org/randomized-algorithms/'
    return render_template("info.html", image=img, heading=heading, text1=text1, text2=text2,text3=text3,link=link,text4=text4)

@app.route("/info-bitwise-algorithms", methods=["GET"])
def bit():
    heading='Bitwise Algorithms'
    text1="Bitwise Algorithms are Algorithms used to perform operations at bit-level or to manipulate bits in different ways. The bitwise operations are found to be much faster and are some times used to improve the efficiency of a program."
    text2="For example: To check if a number is even or odd. This can be easily done by using Bitwise-AND(&) operator. If the last bit of the operator is set than it is ODD otherwise it is EVEN. Therefore, if num & 1 not equals to zero than num is ODD otherwise it is EVEN."
    text4="Operations with bits are used in Data compression (data is compressed by converting it from one representation to another, to reduce the space)  In order to encode, decode or compress files we have to extract the data at bit level. Bitwise Operations are faster and closer to the system and sometimes optimize the program to a good level."
    img="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAdsAAABqCAMAAADDRQtiAAAAyVBMVEX///8AAADs7OxYWFiMjIzJycnQ0NCCgoLNzc3p6emHh4deXl78/PyysrLx8fGmpqb39/fj4+Pc3NzDw8N4eHhycnLV1dVERESvr6+UlJTf39+6urpLS0ufn58vLy9GRkZoaGg6Ojp1dXUsLCxSUlKSkpIcHBw9PT0NDQ0jIyM1NTVjY2MXFxctLS3/6+v/MzP/hYX/AAD/09P/YGD/Jyf/cnL/mJj/e3v/UFD/Pz//4uL/9PT/j4//p6f/tLT/vb3/amr/FRX/VVXjRK6XAAAViklEQVR4nO1dCZujNraV2MQihFgNBmxs4xUn8yaTTLaZN/Pm//+opyuB7Vq67U66qJqE831JV7kQlnR0r4Tu0QWhCRMmTJgwYcKECRMmTJgwYcKECRMmTJgwYcKECRMmTPhA4GHMnn82z+ir19LQenHtBAAzM/mvVQcxf/a3aISvL+ug9l98rNU4e/6Zq2uv36I+2V+/Yp/C/L9nHGnWKYB/fb3Z74In5M6L6u2/n5seXpsvPy/xi4EVWZ+wW2tjffV6fRJFUz41AW72H0QuSfLxKnIfnGKoD6vnLExubUUzZhiPUYMAz1/5NH7J7SfhjMktwceuvPmdW+lacktJmpB4vIo8goMca2ASMb76NveI8Tjc5thBURpk1eFivv7xOANutQQfBW0aORxKNN+6THNTuxODsca6+HPo4WMuKh6Oyy3GB/12wnBTyW0Zq178SDhc/EjcheoHtsUKTHsj3HQCcGsvq3yuD0Mpnzm8E9w661KwGDldIIzbDJOGhc0uRz52Q964HGFX/GxduKVvVtsbsET1zPK6sDMktzzBrflhueXDmoa7u55bT38bVDduGLjlqQFTrPqA4VLNt2VjZRYmZcqQ1mWobhhyKw1pYunEt7qD0oyXG/vCLSPtG1X3Bt6m75r24uMUtyw2PGx8MHIv3Eb+ZQkYE+mSR/PJPN0KT9xPvPYmlNzSonIJMYKaqLWK4tZBzsIU3HqOqOZ2fbBH9smu7Bi9di6fKG4FaH14ueJ/VwzcOvbN6p7GZDc+t2pKMDdRz60Bv4aFsFvxEPuSW6MzrWpsbmG+1YPw5pMLtwilZLyKPIJ+rGnPnjCYTcbktrhym8HKHdbJpVxI+Tks8cLy4pOdhS251cRcGy7t0dfJSz988skNt/l6vIo8AHqQY01Lc9+vnzzg8igdowK1mF75klBBsvLJXF/ZaItLFrbHIqhYNFsEgeDVmDHUCG6jY46osXQcLNZYh8BG1mHER48gf755YawvvfbKLsw7Ij4JF+Og+V5OI+X9Al8ZTgM+rsU4Tc94oThia6wb+5ijyMMzwXdWYZ3TGuNKF8s7WAo0YtY7idV8k6Udt96l4hfw5Aj7ZYFuoyB4v2pM+Ppwkll1FAuEqDlVI259TpgwYcKECRMmTJgwYcKECRPeEzwLLrGVEURbHx7l2pV72LRIa7nlGRqp2oozSTroBKjlK0EZj0v6pNiv//jh79+OW+MB9poQ8kT6prm4171x/KG2aBHKngvyMjdVW6VlQtSGeJ3W8iLHSP0hABPmfQMzX0UHBQFq+P7yz/+99521bgctjPEusQkR5IZtbeqwwVnqZbxQ22E0K3TJJLO6hKpipiz269/+9q9///t9yGUx3j/TWJYDtx9OV2gs6ydVtfQgXoENBXrsL4HANLWMtai+1hZmV6ur5vFO2VlWS5KuMqvv/vn9/9z5yvhsI54QimrM0bwVN+o6imIMYQBBcFH1FSrbPkCVSG7Nodg//vot+u4v/3wa5xtNtbd4HnGydx+M0gsIxqfg2k2sdRHyzxzZxxjkcBwFgoBQF13XtBSZOzWlUIT7WJU96yeZPjRI0V/ucVt8I0aKv8rQTBeDgnScYzFk2KZAMUgToiFSEj/lttiIYqUo9tPPCH37w883hsvy3SjxW4DgltWYETzUzj5GFRYuhsUnn/oHK8AQo4288yHVkEN21sFIMdbRXMfGWJVUkLqLYzkMvTl0LMM5Co6i6uAfvZkgzPA0hLeCidkQrf8Ut+gut2zdMIhqx85C3BEVO2ZLNvc6qqsIpq3eOTzlliWdKvbd9z+Iz/7+1wu3ob8fSXcBENzyGgdZfOiHoL2p5/FizVgomuEfXXu+EfZRNSjb5aLWu7jMmSsMBJUFDFGW2SMha5Rcat+z68vZDhNKQOQjmNaWwGZwdpQ56au+ib+D2wSEJxaOtQWQWByZClivPFS3889wmw7c/ohuuJ3n1Wh6KQD45BhT5Hh9BFT6ZB90F6KHMuFXKNQ3yFi5EFcEC7iGH0WbCrmQCAt3JBjLXguXKorKE2g+BLdup0lu2RIcSbBz5orbWd/E32O36WC3kltht5JbsNsv5pbnbd+ArfE2cJ2n1VfcipWlZ/CeW9FTNtgEcHuKBLcNTDpkC6uH+iQvqjcsq18/R/J2UFq4dHDK/sAtaRS32kxye7HbfV/ut3OLtnto+knMtw3Mtx5nOID51lCqo+xT8y0UE2OP/vzTdb6lttdza5tvhGcrpSu321tuV0+4ZcjQo7C7cst3hT/6IQ3QwjXxZUTJjtVEX9cnmG83JtJ1mG9bMd/CgmeZ9Bf+Dm7LA7RfXO4ehIuqRAfAXU0coWxTQm/0tblwSwhwW54jtbr78a9UrJP/0S8AubUf1Sef1i+4BZ8Mz2vSJytutVOMWCfYDBS3YkmavHbe5E0h1nvmzUOQtirgic1B8U6YkOsxVEA79JqiqhOz5GGQ6Q3cWsu+ytv1o9yitc6l76fnLXc74fOyY+nAAh0Fs/CyTOYBViczWHOUtpNAMWEev/7fj9/+8NMv1/uZ1XjcOljMGwW2UVQRZdH2otDimQleTngeHFDWeQ5bNsILEZM3vfgNHgPGhv9MOBOf7HADqwS3ZfFR1JieCC88MSrDs695pLeWsF/P07yngidHNTH98v1P976Tb1edtHan2bvSSE19JlcmPK+W/VEbup218kE7XFctOBHEi70q9t3ffv7xlyd3jL3DF7f8N6Hct5We6u0y8KqlmnBp3O0bMcCdttVTr90HTVUlWlx1YbDWiqrtpDnw+v0VSrRsl3LrjNd7T+49sWZFJG2WN6t7astZu3Rh2Bb7dgVnmJxk2S6g4//1n59++s9349f7HdWDD8FxP9gZjQlfByw2iw92JHLCV0K42uST2f4xQaNoonbChAkTJkyYMEFh0Pg8Du4XQXj/sj8C/JT0eqmm10u5g14queilNCNVDw4WSc0nxVCWj606K9MkSdO0kN+bdM8zl90BJX4wc2Uhy3fuXf3VYL+DIKQY9FJeYpFE6aVsHSJ7oJfaqM051hZ2B3uwZuubm1gVyyF4j6J8NfYGnmbhkxOV+yOMPO1Lg3U25shxYKAOGqRRkFbBUwdj6ysl1wtmrTKhZJXIsRY2q2HPERmnVJqQlq5UOEQUUzEs5+6B7PhsgfCJX/VSXkORCXqpFUTFlvKGTUWRLbrSWQqC8yNXMiuSwB+d4/ibs3uIXDunzW8pC7H8HuZyPG47jE+3eybxPlaxAkMPbRkrmBGthgiW+NhpVKyAeimTJsR2tZNAAAiKgcwAhfauvvOVxaIXPs28z+ilIBjBqwSi8RB98ZXMCoq9wi11tl+vS16HilxXGNEsXfO512RS/8SK0xGLseqf4xSXGGOIElWKv5AsdrqDmHvGG72/jT0it1JTc7yk9JExPjAhMC5U9DE+rYMYn2AiOsugRoAZYmuDo0YM5vkpvhYTWNw5bf+YXiqSYl/vhALJJjb4oJdCL7ilUXF+8xifVJxkm1aMo3XKQ29Zhi6GEHeGmoXgdmPM3dDeCOdFE+XvtLQWoxMUBea1dopbmr2VkuAGVi9JWfXCCxmb5xCbXwhTNYXh6hXE2yA2L+jjKjafLimi9TKEdGeId42yNSiGHuD2Ib2UkvB4K5TvFbd00NSg59zaxWmE+K1+9PN6X8FMtE05IlJ+wdDc16L0LMbiXlap1jUU9irXGGjsM9lcPKPilgdvpAC6xfakuD30K9AbLZz2qhYOPJPmAcPlIQtl8sx0g0pVTBJ/324/r5eivd1KboXdzga7fZ1ba7saRXchue1aaNyVW1G1yNiud0iK4KDa+xK5alVPA6kbAcf9gttxoHSOZNDKP6SF0zzguzxEoXSc6eJSDG5xj9sH9VLgJli1RpJ4RwyiQS+Fbrnlw+DEnfd20MWKRLacJVC5W25tPWf5+cItMvasl5TRflQW78atWEvh5PogBF3+WS0caFg1XXKLs57bzSChe8huX9NLrWFOmqPsGx/0UrI2rZjeLbE0DiFpco61azFRgWsGrjDtudWcN4So0VIqPHNwKpLbteK2Fj/70icrzub71SATsMCrURAGlTfzbTWebMrDXXbzJC6tE6wkkJkKQXu+hIyYnppv2V6a5noP+w7C5YClMn2NJMmO9ND3uQXhk78Cdo4Gc2EMRccybOUYms0HmaNzzp0OluXlyorOMIaSlqsxRGN8sxbXusPb+2Tq4D3iTr47ilVkenL4XrQ+xzENFnbYYDMqD30qR+NSE+6uTC3pxA8ptgflXjBifqng6TCSZ0YCODOyiRFd92dG5hWcGdGpWD3LyyHlneOJtTM5iQdTYURMh2IH2brFvWcgxItZo/RS6cyQ+wC2V/V6qbYaUhNn3VI+TtNSr8onxfKZ/uQUU7Q+vTW3QaXrs9lSNxjiddWmaduSra5XsUaW8byN555eqXaX1+aLK2fwdLet9GV/XKRY6jP/vWK59tJXZ73qNgsqcNBeGrkJnPXa17bXV3ztzbeNMGy+N6wGNi8uxbh1njmjV94mp7G/8lMg4+0pfimoTRIp7eH+2pVGyrf9Gc3IXQ9DjtdpofaqjHXOb4tBJnxjbAG9wPurCBE8tsZBMSks/pDgBU7+JOGePx+06KOexZ0wYcKEl3Csr41pevscePa1+zv7pCwhJl8b8bQs/Qy0+mv3d/FxH/Em/JFBk9cehTXy4n2Jb1cD96GzQWahtgmYmdy58kOhPuly85CmC6K2Rbx+p7KsFsOeY9gt1D5A3J7KvphS+VyKPQp9X81Op5nsLApBpxeZoEL8yf6u5ZQe7meeHBS75Z6QfVWdTqvuy3cP5Xb44aGjuMEslNdrW/zka8KHj42Vz1tptyclfAr2lRrL68Va7UENnS3gLhqll2oWRq+XOj2ql6KJp8VwSJputqyQZ6sXvqPLs9VVFvab6eEx0BpIhuDP7PCc98UWspjBCu9L/D4tBaGsvKQNQtvHt7EYVnId5mKoKmLEoEjDFXTyYfeFsw/90td9QrwwfsLt3H44/VyHjSfslnsVM6euHlpSL7V3mdJLHXNt0Evpg17qXGsy7Bb3xVBone/FCuAdZxRSKLjySL4wo9kawraQE0FUO1c5EaSER1QghNtCYjEZ4zOaS7HbBnPn86mb5jJElUnpiMZReS5DFDoOc8LQQVqoUfhU/BBKy3bCmx1xd98fGufVsXHgNDlENVaSpAjvh2UjU2W5Q+F28vowZIgyh4p/4Nbi/9xbOUzUgKkCTBYQP/Xv/OOiSuK/kFH4j4ladQtHgwwMwz0lHo4kQfy2CC8FtdOn9VId6KXkgFd6KZejTuqlyi/SS6Htqg+yQ2yeEl3F5vnCQCUkYlAiACp5aFMVm4eMV6rYQhTrZLHrkOTZPb3UHAwfOcIEWfxNzshZ99Aez0wDY1e0xnDyVYyspoGgMfcbfX/pPi0dUgRoxNwR3nNbKQMkw5vGItLoSxux4OC7J6m4Zduu8iIn2ZkrwmO9W3ahsIBzU3J7XyBqJY2uZ6IAzorVSYWjrR1O50t8jFmK49DtnHh5aHLBbVgvb6SvD3MrdRe7ejhDeNVLnQa9VKv0UvS5Xip4qZeSFvuYFs4CTQ3MO1ILN2hqPquFGyR0JyWhu8y4drG4F7+V3PItvLpJEzcOIZmhU4n7JAvhagKHRwcTJeIPgkZfjNl6yNCCahORlfxFc1Eu+uAJt6aSmoipqUZ0fXSof6zDyAPfT8Qs0Kwdd2fbMdoTFC1AdwDBcG1To9DzEdeXDs3PQZidhqxLuwxJMUQsCte6IxoPnx5iOt9fHbHkNgvuIp8p1cI3/Qv5xtBL/U4tnHQtoljPrWU8oJeaH3WXpAcZDxbcRvD6NJQLCkqcybfBcsFt0YieRTz1XLfBvT2GNUfOUXa9RmRCOHTLra2ajGIYC6GouJTWwFhlB+K6M6yp3GGxE9agLyikeGNVoxxmORBmQAYj1vQvteQNQTJrG+SbKAW3MoNRDMp179qrsmci/y7KPnfYsU9sNYJe6qqF++Y3aeEGCZ2sMDcGvdRn3pHasvnOyDK/kjH+C7eZmExKsVzzI8UtC5aJJhrnZ5Y1pKcNNq2uY0jlAtyK9dyh9J/YrSv/zWW2HtF+yC8lZ6kQR+Iu2ZBfyuhq0DdcuK1hLQij2NyJ6a1J+gkm2Gms0EsHBuENtzcZj9CX+uRDMe998hh6Kak9B3OU2vOkUdpz7dhrz/tX1klht3AaUtkYDtrzXNjFElJ8SrUyutFLfe5twWi+k/NtBSt/4HYG3HLXzTN7kcOfuHwTNU9ah3nQJqbcWLi1RPFSWrEmR257TG64Tc+qn3PVfqPn9liKroPxMKeKW6/hjveEW5DEwSi2Jbd9OiPknMp8XhCZ3PiGW3rNQvcl3MJayrguC696qWOoVi6Qq1PppbagvVB6qdXv0UuZRxu8j8qxm83EFzYNlWmI55CJiKgcu+uKivknQk4rXHC94HLyvxZbXlc7zfmuT47Um+o78AHiR+BWNDk+isX6UfEsBpRYO1Mx8xliwc5LtboJpDdmKXhQxS1fyFstJLclbtT9Q7ylYsGXKZ/sC1bQaSmWuzmX7IAu09EVt1Rya8mn7ONc2C34ZDIQR3bClA+wshi4pS+5ffgZaOfePgMp4dOOI2sRI5qm8MpIhiLwJ2krCFB6qRL0UpBPzD2JPv9G6qWolFmhR/RS2zar5eZFm2SJzI29rE2p/C2rWKYHg5rMCluma46rMj6BVRVDMT3JCLmpdZTc0UtFNd5GUZyea0pN3DCnc20HRgWkoRNthDRZLnXTzG8zNO9w2sjdBeqfZOdEKSah5q9i+MVZ5sgx8WoemWQxcMKDWWAlgvxs2cZxC51v7w6pbmstDjhirT4vT2tTPAiUEbPPrcaLpW81W1jf1cxeesNrw6MDE0tzKO8I9y8cWRk5Lg5YvG/61R0zxXP2Y3sm5bOnb7u66KUspZfq0oxIvdSsMAe9VOJF2xRmjJlhN4VooFXl8X7QS4V3vprnyValNN8mgeQocxNphzS+ZoyfG4k850pNQuzXi11guZ/VSxnEJUmSbE2KNIMQ0WdE+n1TNMGRYvbEdS2TJATMVThFX3LGDZLAXBwQN/HjpK9aZqMykferr++ypSVJgJFsLzyq2lkzXddEOSHbCPRcW6esxaOtW4gJlZAcGgMiJMt1k3hLyNAeCiPcDqHVCXEZNQrNFpUvRa371yJk4tf6tykAqE1Ir5dKDKWXKpJeL9V3NnxWr+teL5X4Si/lqmKRqIXxDuKDD6GXAgn66FkbJ4wE8zzie6knjAn7gO8eUZ3w3wnKOZ/EAhMmTJgwYcKECRMmTJgwYcKECRMmTJgwYcKEPwn+H5xe3TX5Bo2jAAAAAElFTkSuQmCC"
    link = "https://www.geeksforgeeks.org/bitwise-algorithms/"
    return render_template("info.html", heading=heading, text1=text1, text2=text2,link=link, image=img,text4=text4)

@app.route("/info-pattern-searching", methods=["GET"])
def pattern():
    heading='Pattern Searching Algorithms'
    text1="Pattern Searching algorithms are used to find a pattern or substring from another bigger string. There are different algorithms. The main goal to design these type of algorithms to reduce the time complexity. The traditional approach may take lots of time to complete the pattern searching task for a longer text."
    text4="Some such algorithms are: Naive Pattern Searching, KMP Algorithm, Rabin-Karp Algorithm etc."
    img="https://media.geeksforgeeks.org/wp-content/cdn-uploads/Pattern-Searching-2-1.png"
    link = "https://www.geeksforgeeks.org/algorithms-gq/pattern-searching/"
    return render_template("info.html", heading=heading, text1=text1,link=link, image=img,text4=text4)


if __name__ == '__main__':
  app.run(debug=True)
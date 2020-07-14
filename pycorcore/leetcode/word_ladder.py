"""
Given two words (start and end), and a dictionary, find the length of shortest transformation
sequence from start to end, such that only one letter can be changed at a time and each
intermediate word must exist in the dictionary. For example, given:

start = "hit"
end = "cog"
dict = ["hot","dot","dog","lot","log"]
One shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog",
the program should return its length 5.
"""

from collections import defaultdict, deque

# Basic strategy:
# Use an undirected graph and do a BFS from start word to end word.
# make an edge between each word if distance is one.
# make a subfunction to compute distance


def calc_dist(str_1, str_2):
    return sum(s1 != s2 for s1,s2 in zip(str_1, str_2))


def solve_word_ladder(start_word, end_word, word_dict):

    edge_list = defaultdict(list)

    # Construct a graph with all words
    all_words = [start_word]
    all_words.extend(word_dict)
    all_words.append(end_word)

    n_words = len(all_words)
    v_status = ['unseen']*n_words

    # Add each edge in a loop
    for i in range(n_words-1):
        for j in range(i+1,n_words):
            dist = calc_dist(all_words[i], all_words[j])
            if dist == 1:
                edge_list[i].append(j)
                edge_list[j].append(i)


    bfs_queue = deque([(0,1)])
    v_status[0] = 'visited'
    word_not_found = start_word != end_word
    path_length = 1

    while word_not_found:

        # Visit the next node in the queue
        try:
            curr_idx, path_length = bfs_queue.popleft()
            v_status[curr_idx] = 'exited'
        except IndexError:  # empty queue
            break

        # Loop over all edges
        for v_idx in edge_list[curr_idx]:

            if v_status[v_idx] != 'unseen':
                continue

            # Check if end_word
            if all_words[v_idx] == end_word:
                word_not_found = False
                path_length += 1
            else:
                # Append vertex to queue
                bfs_queue.append((v_idx, path_length+1))

            v_status[v_idx] = 'visited'

    if word_not_found:
        path_length = -1

    return path_length


def test_word_ladder():
    start_word = "hit"
    end_word = "cog"
    word_dict = ["hot","dot","dog","lot","log"]

    path_length = solve_word_ladder(start_word, end_word, word_dict)

    print("Calculated path length:{}, expected: 5".format(path_length))


if __name__ == "__main__":
    test_word_ladder()


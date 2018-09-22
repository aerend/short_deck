#include <iostream>
#include <fstream>
#include <unordered_map>
#include <random>
#include <algorithm>
#include <stack>
#include <chrono>

const int range_from = 0;
const int range_to = 36; // 35?

struct combination_parameter {
    long long bitmask;
    int currently_active_bits;
    int current_bit;
};


void build_seven_card_strength_lookup(std::string file_name, std::unordered_map<long long, long>& seven_card_strength_lookup) {
    std::string line;
    long long key;
    long value;
    std::size_t separator_index;
    std::ifstream file(file_name);
    if (file.is_open()) {
        while (getline(file, line)) {
            separator_index = line.find(",");
            key = std::stoll(line.substr(0, separator_index));
            value = std::stol(line.substr(separator_index+1));
            seven_card_strength_lookup[key] = value;
        }
    }
}


void build_board_combinations(std::stack<long long>& bitmasks, int max_bits, int active_bits, long long deadmask = 0) {
    long long bitmask;
    int current_bit, currently_active_bits;
    std::stack<combination_parameter> combination_stack;
    combination_parameter parameters = {0, 0, 0};
    combination_stack.push(parameters);
    while (!combination_stack.empty()) {
        parameters = combination_stack.top();
        combination_stack.pop();
        bitmask = parameters.bitmask;
        currently_active_bits = parameters.currently_active_bits;
        current_bit = parameters.current_bit;
        if (deadmask & bitmask) {
            continue;
        } else if (currently_active_bits == active_bits) {
            bitmasks.push(bitmask);
        } else if (currently_active_bits > active_bits) {
            continue;
        } else if (current_bit == max_bits) {
            continue;
        } else {
            parameters.current_bit += 1;
            combination_stack.push(parameters);
            parameters.bitmask |= (1 << current_bit);
            parameters.currently_active_bits += 1;
            combination_stack.push(parameters);
        }
    }
}


void build_random_boards(long long bitmasks[], int number_of_bitmasks, int number_of_cards, long long dead_cards) {
    // TODO: may be faster to only return one random number and call function repeatedly
    // TODO: need to make sure this generates all possible cards
    std::random_device rand_dev;
    std::mt19937 generator(rand_dev());
    std::uniform_int_distribution<int> distr(range_from, range_to);
    int current_number_of_cards;
    long long cards;
    long long card;
    for (int i = 0; i < number_of_bitmasks; i++) {
        current_number_of_cards = 0;
        cards = 0;
        while (current_number_of_cards < number_of_cards) {
            card = (1 << distr(generator));
            if (card & (dead_cards | cards)) {
                continue;
            }
            cards |= card;
            current_number_of_cards += 1;
        }
        bitmasks[i] = cards;
    }
}


void monte_carlo(std::unordered_map<long long, long> &seven_card_strength_lookup, int iterations=10000) {
    long long hand_1 = 36507222016;
    long long hand_2 = 83886080;
    long long boards[iterations];
    build_random_boards(boards, iterations, 5, hand_1 | hand_2);
    long long board, result;
    int wins = 0;
    int losses = 0;
    int ties = 0;

    for (int i = 0; i < iterations; i++) {
        board = boards[i];
        result = seven_card_strength_lookup[board | hand_1] - seven_card_strength_lookup[board | hand_2];
        if (result > 0) {
            wins += 1;
        } else if (result < 0) {
            losses += 1;
        } else {
            ties += 1;
        }
    }
    std::cout << "wins " << wins << std::endl;
    std::cout << "losses " << losses << std::endl;
    std::cout << "ties " << ties << std::endl;
}


void compare_hands(std::unordered_map<long long, long> &seven_card_strength_lookup) {
    auto start = std::chrono::system_clock::now();
    std::chrono::duration<double> lookup_duration = start - start;
    std::stack<long long> boards;
    long long hand_1 = 36507222016;
    long long hand_2 = 83886080;
    build_board_combinations(boards, 36, 5, hand_1 | hand_2);

    long long board, result;
    int wins = 0;
    int losses = 0;
    int ties = 0;
    while (!boards.empty()) {
        board = boards.top();
        boards.pop();
        auto start = std::chrono::system_clock::now();
        result = seven_card_strength_lookup[board | hand_1] - seven_card_strength_lookup[board | hand_2];
        auto end = std::chrono::system_clock::now();
        lookup_duration += end - start;
        if (result > 0) {
            wins += 1;
        } else if (result < 0) {
            losses += 1;
        } else {
            ties += 1;
        }
    }
    std::cout << "wins " << wins << std::endl;
    std::cout << "losses " << losses << std::endl;
    std::cout << "ties " << ties << std::endl;
    std::cout << "lookup duration " << lookup_duration.count() << std::endl;
}


int main() {
    std::string file_name = "seven_card_strength_lookup.csv";
    std::unordered_map<long long, long> seven_card_strength_lookup;
    build_seven_card_strength_lookup(file_name, seven_card_strength_lookup);

    auto start = std::chrono::system_clock::now();
    std::cout << "start" << std::endl;
    compare_hands(seven_card_strength_lookup);
    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> duration_ = end - start;
    std::cout << "Time taken: " << duration_.count() << " s" << std::endl;

    start = std::chrono::system_clock::now();
    std::cout << "start 10k mc" << std::endl;
    monte_carlo(seven_card_strength_lookup, 10000);
    end = std::chrono::system_clock::now();
    duration_ = end - start;
    std::cout << "Time taken: " << duration_.count() << " s" << std::endl;

    start = std::chrono::system_clock::now();
    std::cout << "start 1k mc" << std::endl;
    monte_carlo(seven_card_strength_lookup, 1000);
    end = std::chrono::system_clock::now();
    duration_ = end - start;
    std::cout << "Time taken: " << duration_.count() << " s" << std::endl;

    return 0;
}

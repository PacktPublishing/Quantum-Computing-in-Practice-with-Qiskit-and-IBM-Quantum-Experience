#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 2020

@author: hassi
"""

def simple_search(database, oracle):
    # Simple linear search for an item, returns the position
    for position, post in enumerate(database):
        if post == oracle:
            return position

def plot_results(average,search,values):
    import matplotlib.pyplot as plt
    from statistics import mean 
    print("Average searches to find:", mean(average))
    # Plot the search data
    plt.bar(search, average, align='center', alpha=0.5)
    plt.ylabel('Searches')
    plt.title(str(mean(average))+' average searches\nto find one item among '+str(len(values)))
    plt.axhline(mean(average))
    plt.show()

def main():
    import random
    # Create 'database' and set initial oracle
    values=("00","01","10","11","01","10","11","01","10","11","01","10","11","01","10","11")
    oracle=""
    print("Ch 10: Classical search")
    print("-----------------------")
    print("Searching in a scrambled database with "+str(len(values))+" entries:\n", values)
    while oracle!="Exit":
        average=[]
        search=[]
        oracle=input("\nEnter a two bit string for the two qubit state to search for, such as '10' ('Exit' to stop):\n")
        searches=int(input("Number of searches to test:\n"))
        # Run the search algorithm m number of times
        for m in range(searches):
            # Create unordered database by randomizing the 'values' database
            database=random.sample(values,len(values))
            result=simple_search(database, oracle)
            average.append(result+1)
            search.append(m+1)
        # Display the average number of searches needed to find the item
        plot_results(average,search,values)

if __name__ == '__main__':
    main()
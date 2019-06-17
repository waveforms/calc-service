import json

class create_node:
        def __init__(self, data):
                self.data = data
                self.left = self.right = None
 
def sum_longest_path(root, Sum, Len, maxLen, maxSum):							
	# if true, then we have traversed a 
	# root to leaf path 
	if (not root):
		if (maxLen[0] < Len): 
			maxLen[0] = Len
			maxSum[0] = Sum
		elif (maxLen[0]== Len and
			maxSum[0] < Sum): 
			maxSum[0] = Sum
		return

	# left subtree 
	sum_longest_path(root.left, Sum + root.data, Len + 1, maxLen, maxSum) 

	# right subtree 
	sum_longest_path(root.right, Sum + root.data, Len + 1, maxLen, maxSum) 
 
def max_sum_longest_path(root):
    # if tree is NULL, then Sum is 0 
	if (not root): 
		return 0
	maxSum = [-999999999999] 
	maxLen = [0] 
	sum_longest_path(root, 0, 0, maxLen, maxSum)
	return maxSum[0] 


# jd = """
# {"node_value_display": "1", "id": 1, "member_details": {"node_value": "1", "left_or_right": "root", "number_children": "2"}, "children": [{"node_value_display": "2", "id": 2, "member_details": {"node_value": "2", "left_or_right": "left", "number_children": "1"}, "children": [{"node_value_display": "5", "id": 3, "member_details": {"node_value": "2", "left_or_right": "right", "number_children": "0"}, "children": []}]}, {"node_value_display": "3", "id": 4, "member_details": {"node_value": "3", "left_or_right": "right", "number_children": "0"}, "children": []}]}
# """

def convert_json(jd):
	jdo = jd#json.loads(jd)
	root = create_node(int(jdo['node_value_display']))

	def build_tree(root, children):
		if len(children) > 0:
			for child in children:
				if child['member_details']['left_or_right'] == 'left':
					root.left = create_node(int(child['node_value_display']))
					build_tree(root.left, child['children'])
				else:
					root.right = create_node(int(child['node_value_display']))
					build_tree(root.right, child['children'])

	build_tree(root, jdo['children'])
	sum_lp = max_sum_longest_path(root)
	print("Sum = ", sum_lp)
	return sum_lp
    
if __name__ == '__main__':
	jdo = json.loads(jd)
	root = create_node(int(jdo['node_value_display']))
	def build_tree(root, children):
		if len(children) > 0:
			for child in children:
				if child['member_details']['left_or_right'] == 'left':
					root.left = create_node(int(child['node_value_display']))
					build_tree(root.left, child['children'])
				else:
					root.right =  create_node(int(child['node_value_display']))
					build_tree(root.right, child['children'])
		
	build_tree(root, jdo['children'])
	# root.left = create_node(2)
	# root.right = create_node(3)
	# root.left.right = create_node(5)
	# root.right.left = create_node(6)
	# root.right.right = create_node(7)
	# root.left.right.left = create_node(1)
	# root.left.right.right = create_node(2)
	print("Sum = ", max_sum_longest_path(root))
	


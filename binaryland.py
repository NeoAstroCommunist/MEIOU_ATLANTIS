def btree(lst, form, body):
    if not len(lst):
        return ''
    elif len(lst) == 1:
        return body % lst[0]
    else:
        return form % (lst[int(len(lst)/2)],
                       btree(lst[int(len(lst)/2):], form, body),
                       btree(lst[:int(len(lst)/2)], form, body))
        
if __name__ == "__main__":
        cond = 'check_key={lhs=$inp$ value=%s}'
        body = '$action$_ambient_object=pin_%s'
        form = 'if={limit={%s}%s}else={%s}' % (cond, '%s', '%s')

        with open('SYS-Pin.txt', 'w') as f:
            f.write('POP_ChangePin = { #inp #action\n'+btree([i for i in range(1, <max_provinces from default.map here>)], form, body)+'}')


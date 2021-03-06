# coding=utf-8
__author__="Дина"
__date__ ="$06.04.2010 12:44:25$"
from pystab.stability import is_controllable
from pystab.mechanics import *
from pystab.deformable import *
from pystab.mechanics import solve_slae_by_gauss
from numpy import matrix
import matplotlib.pyplot as plt
from pylab import *
from sympy import (Symbol, Function, symbols, sin, cos, tan, cot,
    solve, series, zeros, Derivative as D, diff, Eq, collect, Matrix, pprint,
    simplify, radsimp, fraction, together, expand)
from sympy.core.basic import *



from pystab.integration.ode import *
from pystab.stability import *


def robot_main():
    t = Symbol('t')
    robot = DeformableFrame('Robot with Two Deformable Wheels', 1, 2)

    q, u, a = robot.define_euler_angles('psi, phi, chi')
    psi, dpsi, d2psi = [], [], []
    phi, dphi, d2phi = [], [], []
    chi, dchi, d2chi = [], [], []
    psi, phi, chi = q['psi'], q['phi'], q['chi']
    dpsi, dphi, dchi = u['psi'], u['phi'], u['chi']
    d2psi, d2phi, d2chi = a['psi'], a['phi'], a['chi']

    q, u, a = robot.add_coordinates('q', 2)
    x, y  = q
    dx, dy = u
    d2x, d2y = a

    robot.exclude_from_accelerations([d2psi[1], d2chi[0], d2chi[1]])

    par = robot.add_parameters('A, l, R1, R2 m1, m2, m, J, C, dR1, dR2, M1, M2')
    A, l, R1, R2, m1, m2, m, J, C, dR1, dR2, M1, M2 = par
    T =  1/2.* m * ((dx * cos(psi[0]) + dy * sin(psi[0]) + A * dpsi[0]) ** 2 + (-dx * sin(psi[0]) + dy * cos(psi[0])) ** 2) + 1/2. * m1 * ((dx * cos(psi[0]) + dy * sin(psi[0]) - l * dpsi[0]) ** 2 + (-dx * sin(psi[0]) + dy * cos(psi[0])) ** 2) + 1/2. * m2 * ((dx * cos(psi[0]) + dy * sin(psi[0]) + l * dpsi[0]) ** 2 + (-dx * sin(psi[0]) + dy * cos(psi[0])) ** 2) + 1/2. * J * dpsi[0] ** 2 + 1/2. * C * (dphi[0] ** 2 + dphi[1] ** 2)
    robot.set_lagrangian(T)

    robot.define_pot_energy()
    MFT = robot.define_main_force_torque([dR1, dR2])
    def_eqns = robot.define_deformation_eqns([dx * cos(psi[0]) + dy * sin(psi[0]) - cos(chi[0]) * (l * dpsi[0] + R1 * dphi[0]), dx * cos(psi[1]) + dy * sin(psi[1]) + cos(chi[1]) * (l * dpsi[1] - R2 * dphi[1])], [-dx * sin(psi[0]) + dy * cos(psi[0]), -dx * sin(psi[1]) + dy * cos(psi[1])], [R1, R2], [dR1, dR2])

    robot.add_joint_forces({x: MFT['Fx'][0] * sin(psi[0]) + MFT['Fx'][1] * sin(psi[1]) - \
        MFT['Fy'][0] * cos(chi[0]) * cos(psi[0]) + MFT['Fy'][1] * cos(chi[1]) * cos(psi[1]) \
        - MFT['Fz'][0] * sin(chi[0]) * cos(psi[0]) - MFT['Fz'][1] * sin(chi[1]) * cos(psi[1]), \
        psi[0]: - MFT['Fx'][0] * l * sin(2 * psi[0]) + MFT['Fx'][1] * l * sin(2 * psi[1]) \
        + MFT['Fy'][0] * cos(chi[0]) * l * cos(2 * psi[0]) + MFT['Fy'][1] * cos(chi[1]) * l * cos(2 * psi[1]) \
        + MFT['Fz'][0] * sin(chi[0]) * l * cos(2 *psi[0]) - MFT['Fz'][1] * l * sin(chi[1]) * cos(2 * psi[1]) \
        + MFT['Mz'][0] + MFT['Mz'][1], \
        y:MFT['Fx'][0] * cos(psi[0]) + MFT['Fx'][1] * cos(psi[1]) + \
        + MFT['Fy'][0] * cos(chi[0]) * sin(psi[0]) - MFT['Fy'][1] * cos(chi[1]) * sin(psi[1]) \
        + MFT['Fz'][0] * sin(chi[0]) * sin(psi[0]) + MFT['Fz'][1] * sin(chi[1]) * sin(psi[1]), \
        phi[0]: MFT['My'][0] - R1 * MFT['Fy'][0], phi[1]: MFT['My'][1] + R2 * MFT['Fy'][1]})
    eqns = robot.form_lagranges_equations(1)
#    len_a = len(robot.a_list)
#    print 'robot.a_list = ', robot.a_list
#    MMM = zeros([len_a, len_a])
#    i = 0
#    j = 0
#    for i in range(len_a):
#        if robot.a_list[i] in eqns.keys():
#            for j in range(len_a):
#                print 'j = ', j
#                print 'robot.a_list[j] = ', robot.a_list[j]
#                print 'eqns[robot.a_list[i]] = ', eqns[robot.a_list[i]]
#                tmp = eqns[robot.a_list[i]]
#                tmp_a = robot.a_list[j]
#                MMM[i,j] = pdiff(tmp, tmp_a)
#                print 'MMM[i,j] = ', MMM[i,j]
#    print 'MMM = ', MMM
#    print 'eqns = ', eqns
#    return
    consts = robot.get_deformation_constants()
    def_q = robot.get_deformation_q()
    def_u = robot.get_deformation_u()

#    vars = def_q.values()
#    vars.extend(def_u.values())
#    vars.extend() dpsi, dphi, dchi, psi, phi, chi, [x, dx, y, dy])

   

    for k in def_eqns.keys():
        eqns[k] = def_eqns[k]

    # вычисление якобиана
#    vars = robot.q_list
#    vars.extend(robot.u_list)
#    print 'vars = ', vars
#    print 'keys() = ', eqns.keys()
#    vals = list(eqns.values())
#
#    m = len(vals)
#    n = len(vars)
#
#
#    JJJ = Matrix(m, n, lambda j, i: pdiff(vals[j], vars[i]))
#    for i in range(m):
#        print JJJ[i,11]
#    return

    eqns[d2psi[1]] = l-l
    eqns[d2chi[0]] = l-l
    eqns[d2chi[1]] = l-l

#    for i in eqns.keys():
#        print i
#        print eqns[i]
#
#    return

    q0, u0 = robot.define_equilibrium_point(eqns)

    manifold = robot.form_equilibrium_manifold_equations(eqns)


    # прямолинейное движение, колеса перпендикулярны плоскости качения
#    p0 = {
#        A: 0.35, l: 1., R1:0.47, R2: 0.47, m1: 0.01, m2: 0.01, m: 5.5, J: 0.337, C : 0.0011, dR1 :0.01, dR2:0.02,
#        consts['alpha'][0]: 566.03, consts['beta'][0]:110.51, consts['gamma'][0]:0.0, consts['N'][0]:3.0, consts['cy'][0]: 147.0, consts['ct'][0]:0.26, consts['nu2'][0]:1.0, consts['rho2'][0]:80.6,
#        consts['alpha'][1]:566.05, consts['beta'][1]:110.53, consts['gamma'][1]:0.0, consts['N'][1]:3.0, consts['cy'][1]:150.0, consts['ct'][1]:0.25, consts['nu2'][1]:1.0, consts['rho2'][1]:80.4,
#        q0[chi[0]]: 0., q0[chi[1]]: 0.,
#        q0[psi[1]]: q0[psi[0]], q0[def_q['eta1'][1]]: 0,
#        q0[def_q['eta1'][0]]:-0.25* 0 /0.26,
#        q0[def_q['eta0'][1]]: 0, q0[def_q['eta0'][0]]: 0,
#        q0[psi[0]]:0.0, u0[dy]: 0., u0[dx]: 4, u0[dphi[0]]:  8.1604869199,
#        u0[dphi[1]]: 8.1604869199
#    }
    # прямолинейное движение, колеса перпендикулярны плоскости качения
#    p0 = {
#        A: 0.35, l: 1., R1:0.47, R2: 0.47, m1: 0.01, m2: 0.01, m: 5.5, J: 0.337, C : 0.0011, dR1 :0.01, dR2:0.02,
#        consts['alpha'][0]: 566.03, consts['beta'][0]:110.51, consts['gamma'][0]:0.0, consts['N'][0]:3.0, consts['cy'][0]: 147.0, consts['ct'][0]:0.26, consts['nu2'][0]:1.0, consts['rho2'][0]:80.6,
#        consts['alpha'][1]:566.05, consts['beta'][1]:110.53, consts['gamma'][1]:0.0, consts['N'][1]:3.0, consts['cy'][1]:150.0, consts['ct'][1]:0.25, consts['nu2'][1]:1.0, consts['rho2'][1]:80.4,
#        q0[chi[0]]: 0., q0[chi[1]]: 0.,
#        q0[psi[1]]: q0[psi[0]], q0[def_q['eta1'][1]]: 0,
#        q0[def_q['eta1'][0]]:-0.25* 0 /0.26,
#        q0[def_q['eta0'][1]]: 0, q0[def_q['eta0'][0]]: 0,
#        q0[psi[0]]:0.06, u0[dy]: 0.23, u0[dx]: 4, u0[dphi[0]]:  8.1604869199,
#        u0[dphi[1]]: 8.1604869199
#    }
    # прямолинейное движение, колеса под углом к плоскости качения
#    p0 = {
#        A: 0.35, l: 1., R1:0.47, R2: 0.47, m1: 0.01, m2: 0.01, m: 5.5, J: 0.337, C : 0.0011, dR1 :0.01, dR2:0.02,
#        consts['alpha'][0]: 566.03, consts['beta'][0]:110.51, consts['gamma'][0]:0.0, consts['N'][0]:3.0, consts['cy'][0]: 147.0, consts['ct'][0]:0.26, consts['nu2'][0]:1.0, consts['rho2'][0]:80.6,
#        consts['alpha'][1]:566.05, consts['beta'][1]:110.53, consts['gamma'][1]:0.0, consts['N'][1]:3.0, consts['cy'][1]:150.0, consts['ct'][1]:0.25, consts['nu2'][1]:1.0, consts['rho2'][1]:80.4,
#        q0[chi[0]]: 0.006, q0[chi[1]]: -0.005,
#        q0[psi[1]]: q0[psi[0]], q0[def_q['eta1'][1]]: -0.000652268462177,
#        q0[def_q['eta1'][0]]:0.000627181213632,
#        q0[def_q['eta0'][1]]: -0.00010000000000000, q0[def_q['eta0'][0]]: 0.000122448979591837,
#        q0[psi[0]]:0.06, u0[dy]: 0.23, u0[dx]: 4, u0[dphi[0]]:  8.16440128832,
#        u0[dphi[1]]: 8.52477439186
#    }
    p0 = {
        A: 0.35, l: 1., R1:0.47, R2: 0.47, m1: 0.01, m2: 0.01, m: 5.5, J: 0.337, C : 0.0011, dR1 :0.01, dR2:0.01,
        consts['alpha'][0]: 566.03, consts['beta'][0]:110.51, consts['gamma'][0]:0.0, consts['N'][0]:3.0, consts['cy'][0]: 147.0, consts['ct'][0]:0.26, consts['nu2'][0]:1.0, consts['rho2'][0]:80.6,
        consts['alpha'][1]:566.03, consts['beta'][1]:110.51, consts['gamma'][1]:0.0, consts['N'][1]:3.0, consts['cy'][1]:147.0, consts['ct'][1]:0.26, consts['nu2'][1]:1.0, consts['rho2'][1]:80.6,
        q0[chi[0]]: 0.006, q0[chi[1]]: -0.006,
        q0[def_q['eta1'][1]]: -0.000627181215722,
        q0[def_q['eta1'][0]]:0.000627181215722,
        q0[def_q['eta0'][1]]: -0.00012244898, q0[def_q['eta0'][0]]: 0.00012244898,
        q0[psi[0]]:0., q0[psi[1]]:0., u0[dy]: 0., u0[dx]: 4., u0[dphi[0]]:  8.6957,
        u0[dphi[1]]: 8.6957
    }


#    for k in manifold.keys():
#        print k
#        print float(manifold[k].subs(p0))
    

#    slv = solve_slae_by_gauss([manifold[def_u['eta0'][0]].subs(p0).subs(p0), manifold[def_u['eta1'][0]].subs(p0).subs(p0)], \
#        #manifold[def_u['eta1'][1]].subs(p0).subs(p0), \
#        #manifold[d2psi[0]]], [q0[def_q['eta1'][0]], q0[def_q['eta1'][1]], u0[dphi[0]], u0[dphi[1]], \
#        [q0[def_q['eta1'][0]], u0[dphi[0]]])
#    print float(slv[u0[dphi[0]]])
#    print float(slv[q0[def_q['eta1'][0]]])
#
#    slv = solve(manifold[def_u['eta0'][1]].subs(p0),q0[def_q['eta1'][1]])
#    print float(slv[0])
#    slv = solve(manifold[d2psi[0]].subs(p0),q0[def_q['eta1'][1]])
#    print float(slv[0])


    pertubed = robot.form_perturbed_equations(eqns, manifold)
    print robot.x_list
    print robot.x
    fa = robot.form_first_approximation_equations(pertubed, q0, u0, params = p0)
    rem_chi = {robot.x_list[8]: 0, robot.x_list[9]: 0, robot.x_list[5]: robot.x_list[4]}
    for k in fa.keys():
        fa[k] = fa[k].subs(rem_chi)
    del(fa[diff(robot.x_list[5] ,t)])
    del(fa[diff(robot.x_list[8] ,t)])
    del(fa[diff(robot.x_list[9] ,t)])
    del(robot.x_list[9])
    del(robot.x_list[8])
    del(robot.x_list[5])
    print fa


#    print '1st approximation eqns: ', fa
    x_0 = [(x, 0) for x in robot.x.values()]

    # РњР°С‚СЂРёС†Р° РєРѕСЌС„С„РёС†РёРµРЅС‚РѕРІ
    dx =  [x.diff(t) for x in robot.x_list]
    fa_eqns_sorted = [fa[k] for k in dx]

    A = robot.create_matrix_of_coeff(fa_eqns_sorted, robot.x_list)

    # порядок удаления важен!!!
#    A.col_del(16)
#    A.row_del(16)
#    A.col_del(13)
#    A.row_del(13)
#    i = 11
#    while i >= 5:
#        A.col_del(i)
#        A.row_del(i)
#        i -= 1
#
#    for i in range(8):
#        for j in range(8):
#            A[i,j] = float(A[i,j])

    print A.tolist()
#    eig = A.eigenvals()
#    print 'len = ', len(eig)
#    for e in eig:
#        print e

    B = matrix([1,1,1,1,1,3,3,2,2,3,1,2,3,1]).transpose()
    MMM = ctrb(A, B)
    print MMM
    MMM1 = Matrix(MMM)
    print matrix_rank(MMM)
    print MMM1.eigenvals()
    print is_controllable(A, B)

    reg = LQRegulator(A, B)
    u = reg.find_control(time = 5., h=1e-2) # time = 0.813620981911
    print u
    return
    u = matrix([ -8.82024754e+01,   6.84254160e+00,   2.35977922e+01,   8.55301959e+00,
    6.17981990e+00,  -3.01406196e-02,  -9.70135476e-02,  -5.26718908e-02,
   -4.57948571e-02,  -3.03742899e-01,  -1.61023300e+00,   3.26998562e-01,
    3.01181956e-02,  -1.29027532e-01])
    def f1(x, t):
        dx = A * matrix(x).transpose()
        return mtx2row(dx)

    def f2(x, t):
        dx = (A + B * u) * matrix(x).transpose()
        return mtx2row(dx)
    x0 = [0.00012244898, -0.00012244898, 0.000627181215722, -0.000627181215722, 0., 0., 0., 0., 0., 8.6957, 0., 0., 8.6957, 4.]
    slv = scipy_odeint(f2, x0, t0=0., t1=5., last=False, h=1e-2)

    #print slv
    #print len(slv[:,0])
    #print slv[:,1]
    t = slv[:, 0]
    x1 = slv[:, 1]
    x2 = slv[:, 2]
    x3 = slv[:, 3]
    x4 = slv[:, 4]
    x5 = slv[:, 5]
    x6 = slv[:, 6]
    x7 = slv[:, 7]
    x8 = slv[:, 8]
    x9 = slv[:, 9]
    dx7 = slv[:, 10]
    dx9 = slv[:, 11]
    dx5 = slv[:, 12]
    dx6 = slv[:, 13]
    dx8 = slv[:, 14]

    plt.figure(1)
    plt.subplot(221)
    plt.plot(x8, x9, label='A position', color='green')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend(loc=2)

    plt.subplot(222)
    plt.plot(t, x8, label='Wheel position x', color='green')
    plt.plot(t, x9, label='Wheel position y', color='blue')
    plt.plot(t, x5, label='Wheel position psi', color='red')
    plt.xlabel('t')
    plt.ylabel('x')
    plt.grid(True)
    plt.legend(loc=2)

    plt.subplot(223)
    plt.plot(t, dx8, label='Velocity x', color='green')
    plt.plot(t, dx9, label='Velocity y', color='blue')
    plt.plot(t, dx5, label='Velocity psi', color='red')
    plt.xlabel('t')
    plt.grid(True)
    plt.legend(loc=2)

    plt.grid(True)
    plt.show()



robot_main()
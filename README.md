# 使用方法：
      （1）git clone 到本地
      （2）进入该文件夹（vancancyMigration的父文件夹），命令行输入“pip install .”
      （3）进入python交互界面
             3.1 from vacancyMigration.vanMig import vacancyMigration1
             3.2 motion = vacancyMigration1(cifFile='输入一个cif文件的路径')   //CONTCAR、POSCAR可以用VESTA转化成cif格式
             3.3 motion.migration_nsteps(center=57, nsteps=5)    // center是空位初始位置，nsteps是扩散步数

# 文件夹介绍：
      （1）vacancyMigration: 主要的python程序（主程序：vanMig.py）
      （2）shell_scripts: 储存脚本，用于处理vanMig.py输出的结果
            generate_structures: 根据vanMig.py输出的 python输出文件/positionOfVacancy 生成新结构
      （3）python输出文件: 程序的输出文件，
            positionOfVacancy: 用于储存count次nsteps步扩散后，空位所在位置
            CONTCAR${num}: 新生成的带有氧空位的结构
      （4）CONTCAR.cif: 完整的初始结构，新结构基于此结构生成

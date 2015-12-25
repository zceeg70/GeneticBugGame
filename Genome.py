__author__ = 'Peter'
import random
import string

SEED = 9283
random.seed(SEED)

class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AlleleAllocation:
    def __init__(self, startIndex, finishIndex, value, owner):
        self.startIndex = startIndex
        self.finishIndex = finishIndex
        self.value = value
        self.owner = owner

class Gene:
    def __init__(self, name, nibbles=16):
        self.name = name
        self.priority = 0 # defines dominance over another gene
        bytes = nibbles*2
        # self.value = "".join(random.SystemRandom().choice(string.ascii_uppercase +
        #                                                   string.digits +
        #                                                   string.ascii_lowercase) for _ in range (length))
        # strChoices = [chr(x) for x in range(ord("0"), ord("z"))]
        # self.value = "".join(random.SystemRandom().choice( strChoices ) for _ in range(length))
        self.value = "".join(hex(random.SystemRandom().randint(0,15))[2] for _ in range(bytes))
        self.allelePointer = 0
        self.alleles = bytes
        self.allocations = []
        # print("{}Value: {}{}".format('\033[92m',self.value,'\033[0m'))

    def allocate_alleles(self, number, owner="UNKNOWN"):
        if self.allelePointer + number > self.alleles:
            return False
        else:
            allocationStart = self.allelePointer
            self.allelePointer += number
            allocationFinish = self.allelePointer
            value = self.value[allocationStart:allocationFinish]
            # print("Value allocated:{}{}{}".format(PrintColors.WARNING,value,PrintColors.ENDC))
            self.allocations.append(AlleleAllocation(allocationStart, allocationFinish, value, owner))
            return value

    def print_allocations(self):
        for allocation in self.allocations:
            print("Owner:{} Value:{} Length:{}".format(allocation.owner, allocation.value, len(allocation.value)))

class Genome:
    def __init__(self):
        self.genes = []

    def add_trait(self,name,allocation=1):
        requireNewGeneFlag = True
        value = False
        for gene in self.genes:
            value = gene.allocate_alleles(allocation, name)
            if value != False:
                requireNewGeneFlag = False
                break
        if requireNewGeneFlag:
            newGene = Gene(str(len(self.genes)+1))
            newGene.allocate_alleles(allocation, name)
            value = self.genes.append(newGene)
        return value

    def get_trait(self,name):
        for gene in self.genes:
            for allocation in gene.allocations:
                if name == allocation.owner:
                    return allocation.value
        return False

def main():
    gen = Genome()
    gen.add_trait("colour", 8)
    gen.add_trait("numberOfLegs",1)


if __name__ == "__main__":
    main()